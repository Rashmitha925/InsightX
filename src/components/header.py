import streamlit as st


def render_header():
    """
    Render the application header.
    """

    st.title("📊 InsightX")
    st.subheader("Intelligent Data Analytics Dashboard")

    st.write("""
    Welcome to InsightX!

    Upload your CSV or Excel dataset to begin your analysis.
    """)