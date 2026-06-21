"""
Answer display component — renders answer with confidence badge and validation status.
"""

import streamlit as st


def render_answer(
    answer: str,
    confidence_score: float,
    validation_status: str,
    hallucination_flags: list[str] | None = None,
    query_type: str = "",
    latency_ms: float = 0.0,
    rewrite_iterations: int = 0,
) -> None:
    """
    Renders the main answer with confidence badge, validation status,
    and hallucination warnings.

    Args:
        answer: Generated answer text with citations.
        confidence_score: Answer confidence 0.0–1.0.
        validation_status: "passed", "warning", or "failed".
        hallucination_flags: List of unsupported claims.
        query_type: Detected query type.
        latency_ms: Total pipeline latency.
        rewrite_iterations: Number of query rewrites performed.
    """
    # Header with metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Confidence", f"{confidence_score:.0%}")
    with col2:
        st.metric("Query Type", query_type.title())
    with col3:
        st.metric("Latency", f"{latency_ms:.0f}ms")
    with col4:
        st.metric("Rewrites", str(rewrite_iterations))

    # Validation status banner
    if validation_status == "passed":
        st.success("✅ Answer validated — all claims supported by source documents")
    elif validation_status == "warning":
        st.warning("⚠️ Answer validated with warnings — some claims may need review")
    else:
        st.error("❌ Validation failed — answer may contain unsupported claims")

    # Answer body
    st.markdown("---")
    st.markdown(answer)

    # Hallucination flags
    if hallucination_flags:
        st.markdown("---")
        st.warning("**⚠️ Hallucination Warnings**")
        for flag in hallucination_flags:
            st.markdown(f"- 🔴 {flag}")


def render_refusal(quality_score: float, rewrite_count: int) -> None:
    """
    Renders a styled refusal message when context is insufficient.

    Args:
        quality_score: Best achieved quality score.
        rewrite_count: Total search attempts.
    """
    st.error("🚫 Insufficient Context")
    st.markdown(
        "The system was unable to find sufficient relevant information "
        "in the data room to answer this question accurately."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Best Quality Score", f"{quality_score:.0%}")
    with col2:
        st.metric("Search Attempts", str(rewrite_count + 1))

    st.info(
        "💡 **Suggestions:**\n"
        "- Check that the relevant documents have been uploaded\n"
        "- Try rephrasing your question with different terminology\n"
        "- Narrow the scope (specific fiscal year, document type)"
    )
