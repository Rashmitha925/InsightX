import streamlit as st
import pandas as pd


def upload_dataset():
    """
    Display the file uploader and return the uploaded dataframe.
    """

    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx"]
    )

    if uploaded_file is None:
        return None

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ Dataset uploaded successfully!")

        return df

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        return None