"""
Risk dashboard component — summarizes risk signals detected during ingestion.
"""

import streamlit as st


def render_risk_dashboard(risk_signals: list[dict]) -> None:
    """
    Renders a dashboard of risk signals detected across deal documents.
    Shows change of control flags, MAC clauses, litigation mentions,
    and PII content warnings.

    Args:
        risk_signals: List of risk signal dicts from ingestion pipeline.
            Each dict has: signal_type, severity, source_file, description, page_number.
    """
    st.subheader("🚨 Risk Signal Dashboard")

    if not risk_signals:
        st.success("✅ No risk signals detected in current documents.")
        return

    # Categorize signals
    categories = {
        "change_of_control": {"icon": "🔄", "label": "Change of Control", "items": []},
        "material_adverse_change": {"icon": "⚠️", "label": "Material Adverse Change", "items": []},
        "litigation": {"icon": "⚖️", "label": "Litigation / Legal Risk", "items": []},
        "pii_content": {"icon": "🔒", "label": "PII Content", "items": []},
        "financial_inconsistency": {"icon": "📊", "label": "Financial Inconsistency", "items": []},
        "other": {"icon": "📋", "label": "Other Signals", "items": []},
    }

    for signal in risk_signals:
        sig_type = signal.get("signal_type", "other")
        if sig_type in categories:
            categories[sig_type]["items"].append(signal)
        else:
            categories["other"]["items"].append(signal)

    # Summary metrics
    high_count = sum(1 for s in risk_signals if s.get("severity") == "high")
    medium_count = sum(1 for s in risk_signals if s.get("severity") == "medium")
    low_count = sum(1 for s in risk_signals if s.get("severity") == "low")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Signals", len(risk_signals))
    with col2:
        st.metric("🔴 High", high_count)
    with col3:
        st.metric("🟡 Medium", medium_count)
    with col4:
        st.metric("🟢 Low", low_count)

    st.markdown("---")

    # Render each category
    for cat_key, cat_info in categories.items():
        items = cat_info["items"]
        if not items:
            continue

        with st.expander(
            f"{cat_info['icon']} {cat_info['label']} ({len(items)})",
            expanded=(any(i.get("severity") == "high" for i in items)),
        ):
            for item in items:
                severity = item.get("severity", "low")
                sev_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(severity, "⚪")
                source = item.get("source_file", "Unknown")
                page = item.get("page_number", "")
                desc = item.get("description", "No description")

                st.markdown(
                    f"{sev_icon} **{source}**"
                    + (f" (p.{page})" if page else "")
                    + f": {desc}"
                )
