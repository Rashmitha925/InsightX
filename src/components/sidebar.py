import streamlit as st


def render_sidebar():
    """
    Renders the InsightX sidebar.
    """

    with st.sidebar:

        # ---------------------------------------------------------------------
        # Logo & Branding
        # ---------------------------------------------------------------------
        st.markdown("# 📊 InsightX")
        st.caption("Enterprise Data Analytics Platform")

        st.divider()

        # ---------------------------------------------------------------------
        # Workflow
        # ---------------------------------------------------------------------
        st.markdown("## 📂 Workflow")

        st.markdown("""
- 📤 Upload Dataset
- 👀 Dataset Preview
- 📊 Dataset Summary
- 🛡️ Data Quality Report
- 📑 Column Explorer
- 📈 Data Visualizations
- 🔗 Correlation Analysis
- 📉 Missing Value Analysis
- 🚨 Outlier Detection
- 📊 Statistical Insights
- 🧹 Data Cleaning
- ⚙️ Feature Engineering
- 🤖 AI Insights
- 📥 Export Dataset
""")

        st.divider()

        # ---------------------------------------------------------------------
        # About
        # ---------------------------------------------------------------------
        st.markdown("## ℹ️ About")

        st.info(
            """
InsightX is an intelligent data analytics platform that helps users
analyze datasets, discover insights, clean data, engineer features,
and generate AI-powered recommendations.
"""
        )

        st.divider()

        # ---------------------------------------------------------------------
        # Developer
        # ---------------------------------------------------------------------
        st.markdown("## 👨‍💻 Developer")

        st.write("**Rashmitha M**")

        st.caption("Version 1.0")

        st.caption("Built with ❤️ using Streamlit")