import streamlit as st
import pandas as pd

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

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ Dataset uploaded successfully!")

        st.write("### Dataset Preview")
        st.dataframe(df.head())

    except Exception as e:
        st.error(f"Error reading file: {e}")