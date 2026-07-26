import streamlit as st
import pandas as pd
import numpy as np


def render_ai_insights(df: pd.DataFrame):
    """
    AI Insight Generator - Phase 2
    """

    st.divider()

    st.header("🤖 AI Insight Generator")

    st.write(
        "Automatically generated insights about your dataset."
    )

    # ==========================================================
    # Dataset Overview
    # ==========================================================

    rows = len(df)
    columns = len(df.columns)

    numeric_columns = len(
        df.select_dtypes(include=np.number).columns
    )

    categorical_columns = len(
        df.select_dtypes(exclude=np.number).columns
    )

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    health_score = 100

    if missing_values > 0:
        health_score -= 10

    if duplicate_rows > 0:
        health_score -= 10

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", rows)
    col2.metric("Columns", columns)
    col3.metric("Health Score", f"{health_score}/100")

    col4, col5 = st.columns(2)

    col4.metric("Numeric Columns", numeric_columns)
    col5.metric("Categorical Columns", categorical_columns)

    # ==========================================================
    # Key Findings
    # ==========================================================

    st.subheader("🔍 Key Findings")

    findings = []

    findings.append(
        f"Dataset contains **{rows} rows** and **{columns} columns**."
    )

    findings.append(
        f"Numeric columns: **{numeric_columns}**"
    )

    findings.append(
        f"Categorical columns: **{categorical_columns}**"
    )

    if missing_values == 0:
        findings.append("✅ No missing values detected.")
    else:
        findings.append(
            f"⚠️ {missing_values} missing values detected."
        )

    if duplicate_rows == 0:
        findings.append("✅ No duplicate rows found.")
    else:
        findings.append(
            f"⚠️ {duplicate_rows} duplicate rows found."
        )

    for item in findings:
        st.write("•", item)

    # ==========================================================
    # Correlation Insights
    # ==========================================================

    st.subheader("🔗 Correlation Insights")

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.shape[1] >= 2:

        corr = numeric_df.corr().abs()

        np.fill_diagonal(corr.values, 0)

        strongest = corr.stack().idxmax()

        value = corr.loc[
            strongest[0],
            strongest[1]
        ]

        st.success(
            f"Strongest correlation detected between "
            f"**{strongest[0]}** and **{strongest[1]}** "
            f"({value:.2f})"
        )

    else:

        st.info(
            "Not enough numeric columns to calculate correlation."
        )

    # ==========================================================
    # AI Recommendations
    # ==========================================================

    st.subheader("💡 AI Recommendations")

    recommendations = []

    if missing_values > 0:
        recommendations.append(
            "Clean missing values before modelling."
        )

    if duplicate_rows > 0:
        recommendations.append(
            "Remove duplicate rows."
        )

    if numeric_columns > 0:
        recommendations.append(
            "Standard Scaling is recommended before machine learning."
        )

    if categorical_columns > 0:
        recommendations.append(
            "Categorical columns can be encoded before modelling."
        )

    if health_score >= 90:
        recommendations.append(
            "Dataset is ready for analysis."
        )

    for recommendation in recommendations:
        st.write("✅", recommendation)