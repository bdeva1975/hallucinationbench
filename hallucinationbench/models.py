from dataclasses import dataclass, field
from typing import List


@dataclass
class ScoreResult:
    """
    The result returned by hallucinationbench.score().

    Attributes:
        faithfulness_score  : float between 0.0 and 1.0.
                              1.0 means fully grounded, 0.0 means fully hallucinated.
        grounded_claims     : list of statements in the response that are
                              supported by the context.
        hallucinated_claims : list of statements in the response that are
                              NOT supported by, or contradict, the context.
        verdict             : "PASS"  → faithfulness_score >= 0.8
                              "WARN"  → faithfulness_score >= 0.5
                              "FAIL"  → faithfulness_score < 0.5
        model               : the OpenAI model used as the judge.
    """

    faithfulness_score: float
    grounded_claims: List[str] = field(default_factory=list)
    hallucinated_claims: List[str] = field(default_factory=list)
    verdict: str = "FAIL"
    model: str = "gpt-4o-mini"

    def __str__(self) -> str:
        lines = [
            f"Verdict          : {self.verdict}",
            f"Faithfulness     : {self.faithfulness_score:.2f}",
            f"",
            f"Grounded claims  ({len(self.grounded_claims)}):",
        ]
        for claim in self.grounded_claims:
            lines.append(f"  ✓  {claim}")

        lines.append(f"")
        lines.append(f"Hallucinated claims  ({len(self.hallucinated_claims)}):")
        for claim in self.hallucinated_claims:
            lines.append(f"  ✗  {claim}")

        return "\n".join(lines)