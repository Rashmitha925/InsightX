import streamlit as st
import pandas as pd

from services.data_profiler import get_dataset_summary

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="InsightX",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Application Header
# --------------------------------------------------
st.title("📊 InsightX")
st.subheader("Intelligent Data Analytics Dashboard")

st.write("""
Welcome to InsightX!

Upload your CSV or Excel dataset to begin your analysis.
""")

# --------------------------------------------------
# File Upload
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)

# --------------------------------------------------
# Read Dataset
# --------------------------------------------------
if uploaded_file is not None:

    try:

        # Read CSV or Excel
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Success Message
        st.success("✅ Dataset uploaded successfully!")

        # Dataset Preview
        st.write("### Dataset Preview")
        st.dataframe(df.head())

        # Dataset Summary
        summary = get_dataset_summary(df)

        st.write("## 📊 Dataset Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", summary["Rows"])
            st.metric("Columns", summary["Columns"])
            st.metric("Missing Values", summary["Missing Values"])

        with col2:
            st.metric("Duplicate Rows", summary["Duplicate Rows"])
            st.metric("Memory Usage (KB)", summary["Memory Usage (KB)"])

    except Exception as e:
        st.error(f"Error reading file: {e}")