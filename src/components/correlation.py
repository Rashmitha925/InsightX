import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


def render_correlation(df: pd.DataFrame):

    st.write("## 🔗 Correlation Dashboard")

    numeric_df = df.select_dtypes(include="number")

    # Need at least two numeric columns
    if numeric_df.shape[1] < 2:
        st.info("At least two numeric columns are required for correlation analysis.")
        return

    correlation_matrix = numeric_df.corr()

    # -----------------------------
    # Correlation Summary
    # -----------------------------

    corr = correlation_matrix.copy()

    np.fill_diagonal(corr.values, np.nan)

    stacked = corr.stack()

    if stacked.empty:
        st.info("No meaningful correlations found.")
        return

    strongest_positive = stacked.idxmax()
    positive_value = stacked.max()

    strongest_negative = stacked.idxmin()
    negative_value = stacked.min()

    st.write("### 📈 Correlation Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Numeric Columns",
            numeric_df.shape[1]
        )

    with col2:
        st.metric(
            "Strongest Positive",
            f"{positive_value:.2f}"
        )
        st.caption(
            f"{strongest_positive[0]} ↔ {strongest_positive[1]}"
        )

    with col3:
        st.metric(
            "Strongest Negative",
            f"{negative_value:.2f}"
        )
        st.caption(
            f"{strongest_negative[0]} ↔ {strongest_negative[1]}"
        )

    st.divider()

    # -----------------------------
    # Heatmap
    # -----------------------------

    fig = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        aspect="auto",
        title="Correlation Heatmap"
    )

    st.plotly_chart(fig, use_container_width=True)