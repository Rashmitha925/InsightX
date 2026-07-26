import streamlit as st
import pandas as pd


def upload_dataset():
    """
    Display the dataset uploader and return the uploaded DataFrame.
    """

    st.markdown("## 📂 Upload Your Dataset")

    st.caption(
        "Upload a CSV or Excel file to start analyzing your data with InsightX."
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Drag and drop your dataset here",
            type=["csv", "xlsx"],
            help="Supported formats: CSV (.csv) and Excel (.xlsx)",
        )

    with col2:
        st.markdown("### 📋 Supported")
        st.success("CSV (.csv)")
        st.success("Excel (.xlsx)")
        st.info("Recommended size:\nUp to 200 MB")
        st.info("🔒 Data is processed locally.")

    if uploaded_file is None:
        st.info("👆 Upload a CSV or Excel file to begin.")
        return None

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(
            f"✅ **{uploaded_file.name}** uploaded successfully!"
        )

        st.write("### Dataset Information")

        info_col1, info_col2, info_col3 = st.columns(3)

        info_col1.metric("Rows", f"{len(df):,}")
        info_col2.metric("Columns", df.shape[1])
        info_col3.metric("File Type", uploaded_file.name.split(".")[-1].upper())

        return df

    except Exception as e:
        st.error(f"❌ Unable to read the uploaded file.\n\n{e}")
        return None