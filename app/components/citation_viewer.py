"""
Citation viewer component — renders citations with version warnings and computed flags.
"""

import streamlit as st


def render_citations(citations: list[dict]) -> None:
    """
    Renders citations with version warnings (⚠ NOT CURRENT VERSION),
    computed metric flags, and source links.

    Args:
        citations: List of citation dicts from QueryResponse.
    """
    if not citations:
        st.caption("No citations available.")
        return

    st.subheader("📚 Source Citations")

    for i, cite in enumerate(citations, 1):
        source = cite.get("source_file", "Unknown")
        page = cite.get("page_number")
        section = cite.get("section_heading", "")
        is_current = cite.get("is_current_version", True)
        content_type = cite.get("content_type", "text")

        # Build citation line
        parts = [f"**{source}**"]
        if section:
            parts.append(f"Section: _{section}_")
        if page:
            parts.append(f"Page {page}")

        # Flags
        flags = []
        if not is_current:
            flags.append("⚠️ NOT CURRENT VERSION")
        if content_type in ("computed_metric", "table_metrics_summary"):
            flags.append("🔢 Computed Metric")
        if cite.get("is_redline"):
            flags.append("📝 Redline")

        flag_str = " | ".join(flags)

        # Render
        col1, col2 = st.columns([4, 2])
        with col1:
            st.markdown(f"{i}. " + " | ".join(parts))
        with col2:
            if flag_str:
                st.caption(flag_str)

        # Version warning detail
        if not is_current:
            superseded_by = cite.get("superseded_by", "a newer version")
            st.caption(
                f"   ↳ This document has been superseded by {superseded_by}. "
                "Information may be outdated."
            )
