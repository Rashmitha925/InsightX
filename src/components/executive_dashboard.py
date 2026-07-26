import streamlit as st
import pandas as pd


def render_executive_dashboard(df):
    """
    Display high-level dataset KPIs.
    """

    st.markdown("## 📊 Executive Dashboard")

    total_rows = len(df)
    total_columns = df.shape[1]
    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    numeric_columns = len(df.select_dtypes(include="number").columns)
    text_columns = len(df.select_dtypes(include="object").columns)

    memory_usage = (
        df.memory_usage(deep=True).sum() / (1024 * 1024)
    )

    total_cells = df.shape[0] * df.shape[1]

    if total_cells > 0:
        quality_score = (
            (total_cells - missing_values) / total_cells
        ) * 100
    else:
        quality_score = 100

    row1 = st.columns(4)

    row1[0].metric("📄 Total Rows", f"{total_rows:,}")
    row1[1].metric("📊 Total Columns", total_columns)
    row1[2].metric("❌ Missing Values", missing_values)
    row1[3].metric("🔁 Duplicate Rows", duplicate_rows)

    row2 = st.columns(4)

    row2[0].metric("🔢 Numeric Columns", numeric_columns)
    row2[1].metric("📝 Text Columns", text_columns)
    row2[2].metric("💾 Memory Usage", f"{memory_usage:.2f} MB")
    row2[3].metric("⭐ Data Quality", f"{quality_score:.1f}%")

    st.divider()