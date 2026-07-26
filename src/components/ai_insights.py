import streamlit as st
import pandas as pd


def render_ai_insights(df: pd.DataFrame):
    """
    AI Insight Generator - Phase 1
    Dataset Overview
    """

    st.divider()

    st.header("🤖 AI Insight Generator")

    st.write(
        "Automatically generated insights about your dataset."
    )

    rows = df.shape[0]
    columns = df.shape[1]

    numeric_columns = len(
        df.select_dtypes(include="number").columns
    )

    categorical_columns = len(
        df.select_dtypes(exclude="number").columns
    )

    missing_values = int(df.isnull().sum().sum())

    duplicate_rows = int(df.duplicated().sum())

    dataset_health = 100

    if missing_values > 0:
        dataset_health -= 10

    if duplicate_rows > 0:
        dataset_health -= 10

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", rows)

    with col2:
        st.metric("Columns", columns)

    with col3:
        st.metric("Health Score", f"{dataset_health}/100")

    col4, col5 = st.columns(2)

    with col4:
        st.metric("Numeric Columns", numeric_columns)

    with col5:
        st.metric("Categorical Columns", categorical_columns)

    st.subheader("AI Observation")

    if dataset_health >= 90:
        st.success(
            "Dataset is clean and ready for analysis."
        )

    elif dataset_health >= 70:
        st.warning(
            "Dataset is usable but could benefit from cleaning."
        )

    else:
        st.error(
            "Dataset quality is poor. Cleaning is recommended."
        )