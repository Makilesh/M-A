"""
Query interface component — query input with type hints and controls.
"""

import streamlit as st


EXAMPLE_QUERIES = {
    "Financial": "What was the total revenue in FY2023 and how does it compare to FY2022?",
    "Legal": "What are the key change of control provisions in the merger agreement?",
    "Comparative": "Compare the EBITDA margins across the last three fiscal years.",
    "Summary": "Summarize the key findings from the most recent board minutes.",
    "Multi-hop": "What indemnification caps are tied to the representations that reference FY2023 financials?",
}


def render_query_interface() -> tuple[str, bool] | None:
    """
    Renders query input area with type hints, example queries,
    PII checkbox, and submit button.

    Returns:
        Tuple of (query_text, include_pii) if submitted, None otherwise.
    """
    # Example queries
    with st.expander("💡 Example Queries", expanded=False):
        for category, example in EXAMPLE_QUERIES.items():
            col1, col2 = st.columns([1, 5])
            with col1:
                st.caption(f"**{category}**")
            with col2:
                if st.button(example, key=f"example_{category}", use_container_width=True):
                    st.session_state["query_text"] = example

    # Query input
    query = st.text_area(
        "Ask a question about the deal:",
        value=st.session_state.get("query_text", ""),
        placeholder="Type your M&A due diligence question here...",
        height=100,
        key="query_input",
    )

    # Controls
    col1, col2, col3 = st.columns([2, 2, 4])
    with col1:
        submit = st.button("🔎 Search", type="primary", disabled=not query)
    with col2:
        include_pii = st.checkbox(
            "Include PII",
            value=False,
            help="Include PII-flagged content (HR data, salary info). Requires authorization.",
        )
    with col3:
        st.caption(
            "Results include source citations. "
            "Non-current document versions are flagged."
        )

    if submit and query:
        return query.strip(), include_pii

    return None
