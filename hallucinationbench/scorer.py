import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from hallucinationbench.models import ScoreResult

load_dotenv()

_client = None


def _get_client() -> OpenAI:
    """Lazy-initialise the OpenAI client once."""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "OPENAI_API_KEY not found. "
                "Set it in your .env file or as an environment variable."
            )
        _client = OpenAI(api_key=api_key)
    return _client


_SYSTEM_PROMPT = """
You are a hallucination detection judge.

Your job is to evaluate whether an AI-generated response is faithful to a 
given context. A response is faithful if every factual claim it makes is 
directly supported by the context. A claim is hallucinated if it introduces 
facts, figures, names, or statements that are absent from or contradict 
the context.

You must respond ONLY with a valid JSON object. No explanation. No markdown.
No code fences. Raw JSON only.

The JSON must follow this exact schema:
{
  "grounded_claims": ["claim 1", "claim 2"],
  "hallucinated_claims": ["claim A", "claim B"],
  "faithfulness_score": 0.75
}

Rules:
- Break the response into individual factual claims.
- For each claim, decide: grounded (supported by context) or hallucinated.
- faithfulness_score = grounded_claims / total_claims.
  If there are no claims at all, set faithfulness_score to 1.0.
- Keep each claim as a short, self-contained sentence.
- Do not include opinions, hedges, or non-factual statements as claims.
""".strip()


def _build_user_prompt(context: str, response: str) -> str:
    return (
        f"CONTEXT:\n{context.strip()}\n\n"
        f"RESPONSE TO EVALUATE:\n{response.strip()}"
    )


def _parse_result(raw_json: str, model: str) -> ScoreResult:
    """Parse the JSON returned by the judge into a ScoreResult."""
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Judge returned invalid JSON.\n"
            f"Raw output: {raw_json}\n"
            f"Error: {e}"
        )

    grounded = data.get("grounded_claims", [])
    hallucinated = data.get("hallucinated_claims", [])
    score = float(data.get("faithfulness_score", 0.0))

    # Clamp to [0.0, 1.0] defensively
    score = max(0.0, min(1.0, score))

    if score >= 0.8:
        verdict = "PASS"
    elif score >= 0.5:
        verdict = "WARN"
    else:
        verdict = "FAIL"

    return ScoreResult(
        faithfulness_score=score,
        grounded_claims=grounded,
        hallucinated_claims=hallucinated,
        verdict=verdict,
        model=model,
    )


def score(
    context: str,
    response: str,
    model: str = "gpt-4o-mini",
) -> ScoreResult:
    """
    Evaluate whether an LLM response is faithful to the provided context.

    Args:
        context  : The source text the response should be grounded in.
                   Typically your retrieved RAG documents.
        response : The LLM-generated response to evaluate.
        model    : OpenAI model to use as the judge.
                   Default: "gpt-4o-mini" (fast and cheap).

    Returns:
        ScoreResult with faithfulness_score, grounded_claims,
        hallucinated_claims, and verdict.

    Example:
        from hallucinationbench import score

        result = score(
            context="The Eiffel Tower is located in Paris, France.",
            response="The Eiffel Tower is in Paris. It was built in 1889."
        )
        print(result)
    """
    if not context or not context.strip():
        raise ValueError("context cannot be empty.")
    if not response or not response.strip():
        raise ValueError("response cannot be empty.")

    client = _get_client()

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(context, response)},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    raw_json = completion.choices[0].message.content
    return _parse_result(raw_json, model)