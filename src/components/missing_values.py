import streamlit as st
import pandas as pd
import plotly.express as px


def render_missing_values(df: pd.DataFrame):

    st.write("## 🧹 Missing Value Dashboard")

    missing = df.isnull().sum()

    missing = missing[missing > 0]

    if missing.empty:
        st.success("✅ No missing values found in this dataset.")
        return

    missing_df = pd.DataFrame({
        "Column": missing.index,
        "Missing Values": missing.values
    })

    missing_df["Missing Percentage"] = (
        missing_df["Missing Values"] / len(df) * 100
    ).round(2)

    total_missing = int(missing_df["Missing Values"].sum())

    worst_column = missing_df.sort_values(
        "Missing Values",
        ascending=False
    ).iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Missing Values",
            total_missing
        )

    with col2:
        st.metric(
            "Columns with Missing Values",
            len(missing_df)
        )

    with col3:
        st.metric(
            "Worst Column",
            worst_column["Column"]
        )

    st.divider()

    st.write("### 📋 Missing Value Details")

    st.dataframe(
        missing_df,
        use_container_width=True
    )

    st.write("### 📊 Missing Values by Column")

    fig = px.bar(
        missing_df,
        x="Column",
        y="Missing Values",
        text="Missing Values",
        color="Missing Values",
        title="Missing Values by Column"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )