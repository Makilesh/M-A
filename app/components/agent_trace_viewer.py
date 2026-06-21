"""
Agent trace viewer component — renders execution trace as expandable timeline.
"""

import streamlit as st


def render_agent_trace(trace_data: list[dict]) -> None:
    """
    Renders the agent execution trace as an expandable timeline.

    Each trace entry shows the agent name, model used, latency,
    and key input/output data.

    Args:
        trace_data: List of trace dicts from AgentState.agent_trace.
    """
    if not trace_data:
        st.info("No agent trace available.")
        return

    st.subheader("🔍 Agent Execution Trace")

    for i, entry in enumerate(trace_data):
        agent_name = entry.get("agent", "unknown")
        model = entry.get("model", "—")
        elapsed = entry.get("elapsed_ms", "—")

        # Icon mapping
        icons = {
            "query_intelligence": "🧠",
            "retrieval_executor": "🔎",
            "financial_verifier": "📊",
            "quality_assessor": "✅",
            "query_rewriter": "✏️",
            "answer_synthesizer": "📝",
            "hallucination_validator": "🛡️",
            "insufficient_context": "⚠️",
        }
        icon = icons.get(agent_name, "⚙️")

        with st.expander(
            f"{icon} Step {i + 1}: {agent_name.replace('_', ' ').title()}"
            + (f" — {elapsed}ms" if isinstance(elapsed, (int, float)) else ""),
            expanded=False,
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"**Agent:** {agent_name}")
                if model != "—":
                    st.caption(f"**Model:** `{model}`")
            with col2:
                if isinstance(elapsed, (int, float)):
                    st.caption(f"**Latency:** {elapsed:.0f}ms")

                if entry.get("skipped"):
                    st.info(f"Skipped: {entry.get('reason', 'N/A')}")

            # Show relevant details per agent type
            if agent_name == "query_intelligence":
                if entry.get("output"):
                    output = entry["output"]
                    st.markdown(f"**Query Type:** `{output.get('query_type', '?')}`")
                    if output.get("query_expansions"):
                        st.markdown("**Expansions:**")
                        for exp in output["query_expansions"]:
                            st.markdown(f"  - {exp}")

            elif agent_name == "retrieval_executor":
                st.markdown(
                    f"Dense: {entry.get('dense_count', '?')} | "
                    f"Reranked: {entry.get('reranked_count', '?')}"
                )

            elif agent_name == "quality_assessor":
                score = entry.get("score", 0)
                method = entry.get("method", "?")
                st.markdown(f"**Score:** {score:.2f} ({method})")

            elif agent_name == "query_rewriter":
                st.markdown(
                    f"**Iteration:** {entry.get('iteration', '?')}/2"
                )
                if entry.get("rewritten_query"):
                    st.markdown(f"**Rewritten:** {entry['rewritten_query']}")

            elif agent_name == "hallucination_validator":
                st.markdown(
                    f"**Status:** {entry.get('validation_status', '?')} | "
                    f"**Confidence:** {entry.get('confidence_score', 0):.0%}"
                )

            # Raw JSON fallback
            with st.expander("Raw JSON", expanded=False):
                st.json(entry)
