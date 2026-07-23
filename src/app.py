import streamlit as st
import pandas as pd

from services.data_profiler import get_dataset_summary
from services.data_quality import evaluate_data_quality


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="InsightX",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Header
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
# Dataset Processing
# --------------------------------------------------
if uploaded_file is not None:

    try:

        # Read the uploaded file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Success Message
        st.success("✅ Dataset uploaded successfully!")

        # Dataset Preview
        st.write("## 📄 Dataset Preview")
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

        # --------------------------------------------------
        # Data Quality Analysis
        # --------------------------------------------------

        quality = evaluate_data_quality(df)

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

        col3, col4 = st.columns(2)

        with col3:
            st.metric(
                "Numeric Columns",
                quality["Numeric Columns"]
            )

            st.metric(
                "Missing Values",
                quality["Missing Values"]
            )

        with col4:
            st.metric(
                "Categorical Columns",
                quality["Categorical Columns"]
            )

            st.metric(
                "Duplicate Rows",
                quality["Duplicate Rows"]
            )

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")