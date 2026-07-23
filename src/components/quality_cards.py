import streamlit as st


def render_quality_report(quality: dict):
    """
    Display the data quality report.
    """

    st.write("## 🛡️ Data Quality Report")

    score = quality["Score"]

    if score >= 90:
        st.success(
            f"Quality Score: {score}/100 ({quality['Quality']})"
        )

    elif score >= 70:
        st.warning(
            f"Quality Score: {score}/100 ({quality['Quality']})"
        )

    else:
        st.error(
            f"Quality Score: {score}/100 ({quality['Quality']})"
        )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Numeric Columns",
            quality["Numeric Columns"]
        )

        st.metric(
            "Missing Values",
            quality["Missing Values"]
        )

    with col2:
        st.metric(
            "Categorical Columns",
            quality["Categorical Columns"]
        )

        st.metric(
            "Duplicate Rows",
            quality["Duplicate Rows"]
        )