"""
Streamlit UI — M&A Due Diligence Intelligence Engine.

Sidebar: live budget status display, deal selector.
Main: query interface with citation viewer, version warnings, computed metric flags.
"""

import streamlit as st
import requests
import json

# API base URL
API_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="M&A Due Diligence Intelligence Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    """Main Streamlit application."""

    # ==================== Sidebar ====================
    with st.sidebar:
        st.title("⚙️ Control Panel")

        # Deal selector
        st.subheader("📁 Deal Selection")
        deal_id = st.text_input("Deal ID", value="", placeholder="Enter or select deal ID")

        if st.button("Create New Deal"):
            deal_name = st.text_input("Deal Name", key="new_deal_name")
            if deal_name:
                try:
                    resp = requests.post(
                        f"{API_URL}/deals",
                        json={"deal_name": deal_name, "description": ""},
                    )
                    if resp.status_code == 200:
                        st.success(f"Deal created: {resp.json()['deal_id']}")
                except Exception as e:
                    st.error(f"Failed to create deal: {e}")

        st.divider()

        # Budget status
        st.subheader("💰 API Budget Status")
        try:
            resp = requests.get(f"{API_URL}/budget")
            if resp.status_code == 200:
                budget = resp.json()
                for model_key, status in budget.items():
                    remaining = status.get("remaining", 0)
                    limit = status.get("limit", 0)
                    used = status.get("used", 0)
                    pct = (used / limit * 100) if limit > 0 else 0

                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.caption(model_key.replace("_", " ").title())
                    with col2:
                        st.caption(f"{remaining}/{limit}")

                    color = "normal" if pct < 80 else "inverse" if pct < 95 else "off"
                    st.progress(min(pct / 100, 1.0))
        except Exception:
            st.warning("⚠ Could not fetch budget status")

        st.divider()

        # Document upload
        st.subheader("📄 Document Upload")
        uploaded_file = st.file_uploader(
            "Upload document",
            type=["pdf", "docx", "pptx", "xlsx", "xls"],
        )
        if uploaded_file and deal_id:
            if st.button("📤 Ingest Document"):
                with st.spinner("Ingesting document..."):
                    try:
                        resp = requests.post(
                            f"{API_URL}/ingest",
                            files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                            data={"deal_id": deal_id},
                        )
                        if resp.status_code == 200:
                            result = resp.json()
                            st.success(
                                f"✅ Ingested: {result['chunks_created']} chunks "
                                f"({result['document_category']})"
                            )
                        else:
                            st.error(f"Ingestion failed: {resp.text}")
                    except Exception as e:
                        st.error(f"Upload error: {e}")

    # ==================== Main Content ====================
    st.title("🔍 M&A Due Diligence Intelligence Engine")
    st.caption("Ask questions about your deal documents with traceable citations")

    # Query input
    query = st.text_area(
        "Ask a question about the deal:",
        placeholder="e.g., What was the total revenue in FY2023 and how does it compare to FY2022?",
        height=100,
    )

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        submit = st.button("🔎 Search", type="primary", disabled=not deal_id)
    with col2:
        include_pii = st.checkbox("Include PII", value=False, help="Include PII-flagged content")

    if submit and query and deal_id:
        with st.spinner("Running query pipeline..."):
            try:
                resp = requests.post(
                    f"{API_URL}/query",
                    json={
                        "query": query,
                        "deal_id": deal_id,
                        "include_pii": include_pii,
                    },
                )

                if resp.status_code == 200:
                    result = resp.json()

                    # Answer display
                    st.subheader("📋 Answer")

                    # Validation status badge
                    status = result.get("validation_status", "passed")
                    if status == "passed":
                        st.success(f"✅ Confidence: {result['confidence_score']:.0%}")
                    elif status == "warning":
                        st.warning(f"⚠ Confidence: {result['confidence_score']:.0%}")
                    else:
                        st.error(f"❌ Confidence: {result['confidence_score']:.0%}")

                    st.markdown(result["answer"])

                    # Hallucination flags
                    if result.get("hallucination_flags"):
                        st.warning("⚠ **Hallucination Warnings:**")
                        for flag in result["hallucination_flags"]:
                            st.markdown(f"- {flag}")

                    # Citations
                    if result.get("citations"):
                        st.subheader("📚 Citations")
                        for i, citation in enumerate(result["citations"], 1):
                            version_warning = ""
                            if not citation.get("is_current_version", True):
                                version_warning = " ⚠ NOT CURRENT VERSION"

                            st.markdown(
                                f"{i}. **{citation.get('source_file', 'Unknown')}** "
                                f"| Section: {citation.get('section_heading', 'N/A')} "
                                f"| Page: {citation.get('page_number', 'N/A')}"
                                f"{version_warning}"
                            )

                    # Metadata expander
                    with st.expander("🔧 Query Metadata"):
                        mcol1, mcol2, mcol3 = st.columns(3)
                        with mcol1:
                            st.metric("Query Type", result["query_type"])
                        with mcol2:
                            st.metric("Latency", f"{result['total_latency_ms']:.0f}ms")
                        with mcol3:
                            st.metric("Rewrites", result.get("rewrite_iterations", 0))

                    # Agent trace
                    with st.expander("🔍 Agent Execution Trace"):
                        for trace in result.get("agent_trace", []):
                            st.json(trace)

                else:
                    st.error(f"Query failed: {resp.text}")

            except requests.ConnectionError:
                st.error("❌ Cannot connect to API server. Is it running?")
            except Exception as e:
                st.error(f"Error: {e}")

    elif not deal_id:
        st.info("👈 Enter a Deal ID in the sidebar to get started.")


if __name__ == "__main__":
    main()
