"""
Version browser component — document version history viewer.
"""

import streamlit as st


def render_version_browser(version_chain: list[dict]) -> None:
    """
    Renders document version history showing version chain,
    supersedes relationships, and redline availability.

    Args:
        version_chain: List of version dicts ordered newest-first.
            Each dict has: doc_id, filename, version_label, upload_date,
            is_current_version, supersedes_doc_id, has_redline.
    """
    st.subheader("📋 Document Version History")

    if not version_chain:
        st.info("No version history available for this document.")
        return

    for i, version in enumerate(version_chain):
        is_current = version.get("is_current_version", False)
        doc_id = version.get("doc_id", "?")
        filename = version.get("filename", "Unknown")
        label = version.get("version_label", f"v{len(version_chain) - i}")
        date = version.get("upload_date", "")
        supersedes = version.get("supersedes_doc_id", "")
        has_redline = version.get("has_redline", False)

        # Version badge
        if is_current:
            badge = "🟢 **CURRENT**"
        else:
            badge = "🔴 Superseded"

        with st.expander(
            f"{badge} | {filename} ({label})",
            expanded=is_current,
        ):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"**Doc ID:** `{doc_id[:12]}...`")
            with col2:
                st.caption(f"**Uploaded:** {date}")
            with col3:
                if has_redline:
                    st.caption("📝 Redline available")

            if supersedes:
                st.caption(f"↳ Supersedes: `{supersedes[:12]}...`")

            if not is_current:
                st.warning(
                    "This version has been superseded. "
                    "Citations from this document will show a version warning."
                )

        # Draw connecting line between versions (except last)
        if i < len(version_chain) - 1:
            st.markdown(
                "<div style='text-align: center; color: #666; font-size: 18px;'>↓</div>",
                unsafe_allow_html=True,
            )
