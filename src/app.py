import streamlit as st

st.set_page_config(
    page_title="InsightX",
    page_icon="📊",
    layout="wide"
)

st.title("📊 InsightX")
st.subheader("Intelligent Data Analytics Dashboard")

st.write(
    """
    Welcome to InsightX!

    This application will help users:
    - Upload CSV and Excel files
    - Clean datasets
    - Perform Exploratory Data Analysis (EDA)
    - Generate interactive visualizations
    - Produce AI-powered business insights
    """
)