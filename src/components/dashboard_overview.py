import streamlit as st
import pandas as pd


def render_dashboard_overview(df):
    """
    Displays visual dashboard insights about the uploaded dataset.
    """

    st.markdown("## 📈 Dashboard Overview")

    col1, col2 = st.columns(2)

    # -------------------------------
    # Missing Values by Column
    # -------------------------------
    with col1:
        st.subheader("📉 Missing Values")

        missing = df.isnull().sum()
        missing = missing[missing > 0]

        if len(missing) == 0:
            st.success("✅ No missing values found.")
        else:
            st.bar_chart(missing)

    # -------------------------------
    # Column Type Distribution
    # -------------------------------
    with col2:
        st.subheader("🧩 Column Types")

        column_types = df.dtypes.astype(str).value_counts()

        st.bar_chart(column_types)

    st.divider()

    # -------------------------------
    # Dataset Information
    # -------------------------------

    total_rows = len(df)

    if total_rows < 1000:
        dataset_size = "🟢 Small Dataset"
    elif total_rows < 100000:
        dataset_size = "🟡 Medium Dataset"
    else:
        dataset_size = "🔴 Large Dataset"

    st.info(f"**Dataset Category:** {dataset_size}")

    st.divider()