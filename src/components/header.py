import streamlit as st


def render_header():
    """
    Render the InsightX application header.
    """

    st.container()

    col1, col2, col3 = st.columns([1, 6, 1])

    with col2:

        st.title("📊 InsightX")

        st.caption("Enterprise Data Analytics Platform")

        st.markdown(
            "Upload • Analyze • Clean • Engineer Features • Generate AI Insights"
        )

    st.info(
        "👋 Welcome! Upload a CSV or Excel dataset to begin exploring insights."
    )

    st.divider()