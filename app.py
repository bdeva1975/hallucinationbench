import streamlit as st
from hallucinationbench import score

st.set_page_config(
    page_title="HallucinationBench",
    page_icon="🔬",
    layout="centered",
)

st.title("🔬 HallucinationBench")
st.caption("Detect hallucinations in your RAG pipeline output — in seconds.")

st.divider()

context = st.text_area(
    label="📄 Context",
    placeholder="Paste your retrieved source documents here...",
    height=200,
)

response = st.text_area(
    label="🤖 LLM Response to Evaluate",
    placeholder="Paste the LLM-generated response here...",
    height=150,
)

run = st.button("🔍 Evaluate", use_container_width=True, type="primary")

if run:
    if not context.strip():
        st.warning("Please provide a context.")
    elif not response.strip():
        st.warning("Please provide a response to evaluate.")
    else:
        with st.spinner("Evaluating with GPT-4o-mini..."):
            try:
                result = score(context=context, response=response)

                # Verdict banner
                if result.verdict == "PASS":
                    st.success(f"✅  PASS — Faithfulness Score: {result.faithfulness_score:.2f}")
                elif result.verdict == "WARN":
                    st.warning(f"⚠️  WARN — Faithfulness Score: {result.faithfulness_score:.2f}")
                else:
                    st.error(f"❌  FAIL — Faithfulness Score: {result.faithfulness_score:.2f}")

                st.divider()

                # Grounded claims
                st.subheader(f"✓ Grounded Claims ({len(result.grounded_claims)})")
                if result.grounded_claims:
                    for claim in result.grounded_claims:
                        st.success(claim)
                else:
                    st.info("No grounded claims found.")

                # Hallucinated claims
                st.subheader(f"✗ Hallucinated Claims ({len(result.hallucinated_claims)})")
                if result.hallucinated_claims:
                    for claim in result.hallucinated_claims:
                        st.error(claim)
                else:
                    st.info("No hallucinated claims detected.")

                st.divider()
                st.caption(f"Judge model: `{result.model}`")

            except Exception as e:
                st.error(f"Error: {e}")