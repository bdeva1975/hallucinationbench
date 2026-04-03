# 🔬 HallucinationBench

**Detect hallucinations in your RAG pipeline output — in two lines of Python.**

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![OpenAI](https://img.shields.io/badge/powered%20by-OpenAI-412991)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![OpenAI](https://img.shields.io/badge/powered%20by-OpenAI-412991)
![PyPI](https://img.shields.io/pypi/v/hallucinationbench)

## Installation
```bash
pip install hallucinationbench
```

---

## The problem

Your RAG pipeline retrieves documents and passes them to an LLM.
The LLM generates a response that *sounds* correct.
But is every claim actually grounded in your context — or did the model fabricate some of it?

**HallucinationBench answers that question instantly.**

---

## Quickstart

Install dependencies:

```bash
pip install openai python-dotenv
```

Set your OpenAI API key:

```bash
# .env
OPENAI_API_KEY=your_key_here
```

Run your first evaluation:

```python
from hallucinationbench import score

context = """
The Eiffel Tower is located in Paris, France. It was constructed between
1887 and 1889 as the entrance arch for the 1889 World's Fair.
The tower is 330 metres tall.
"""

response = """
The Eiffel Tower is in Paris. It was built in 1889 and stands 330 metres
tall. It was designed by Leonardo da Vinci and attracts over 7 million
visitors every year.
"""

result = score(context=context, response=response)
print(result)
```

Output:

```
Verdict          : FAIL
Faithfulness     : 0.40

Grounded claims  (2):
  ✓  The Eiffel Tower is in Paris.
  ✓  It stands 330 metres tall.

Hallucinated claims  (3):
  ✗  It was built in 1889.
  ✗  It was designed by Leonardo da Vinci.
  ✗  It attracts over 7 million visitors every year.
```

---

## The result object

```python
result.faithfulness_score    # float 0.0 – 1.0
result.grounded_claims       # list of supported statements
result.hallucinated_claims   # list of fabricated statements
result.verdict               # "PASS" | "WARN" | "FAIL"
result.model                 # judge model used
```

| Verdict | Faithfulness Score |
|---------|-------------------|
| ✅ PASS  | >= 0.8            |
| ⚠️ WARN  | >= 0.5            |
| ❌ FAIL  | < 0.5             |

---

## Streamlit demo

Run the interactive demo locally:

```bash
streamlit run app.py
```

Paste any context and LLM response — get an instant hallucination report.

---

## How it works

1. Your `context` and `response` are sent to `gpt-4o-mini` as a structured judge prompt.
2. The judge breaks the response into individual factual claims.
3. Each claim is classified as grounded (supported by context) or hallucinated (absent or contradicted).
4. A faithfulness score is calculated: `grounded_claims / total_claims`.
5. A verdict of PASS, WARN, or FAIL is assigned.

The judge uses `response_format: json_object` to guarantee structured output.
Temperature is set to 0 for deterministic results.

---

## Cost

Each evaluation uses `gpt-4o-mini`.
Typical cost: **~$0.001 per evaluation** (well under a tenth of a cent).

---

## Roadmap

- [ ] Batch evaluation across multiple context/response pairs
- [ ] CSV upload support in the Streamlit app
- [ ] Custom judge model selection
- [ ] LangChain and LlamaIndex integration hooks
- [ ] CI/CD integration example (GitHub Actions)

---

## Project structure

```
hallucinationbench/
├── hallucinationbench/
│   ├── __init__.py       # public API
│   ├── scorer.py         # GPT-4o-mini judge
│   └── models.py         # ScoreResult dataclass
├── app.py                # Streamlit demo
├── example.py            # quickstart example
├── requirements.txt
├── .env.example
└── README.md
```

---

## License

MIT — free to use, modify, and distribute.

---

## Contributing

Pull requests are welcome. Please open an issue first to discuss what you would like to change.

---

*Built with OpenAI GPT-4o-mini as the hallucination judge.*
