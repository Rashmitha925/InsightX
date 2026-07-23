import streamlit as st
import pandas as pd
import plotly.express as px


def render_outlier_dashboard(df: pd.DataFrame):

    st.divider()

    st.header("📦 Outlier Detection Dashboard")

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        st.info("No numeric columns found.")
        return

    outlier_summary = []

    for column in numeric_df.columns:

        q1 = numeric_df[column].quantile(0.25)
        q3 = numeric_df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - (1.5 * iqr)
        upper = q3 + (1.5 * iqr)

        outliers = numeric_df[
            (numeric_df[column] < lower)
            | (numeric_df[column] > upper)
        ]

        outlier_summary.append(
            {
                "Column": column,
                "Outliers": len(outliers),
                "Percentage": round(
                    (len(outliers) / len(df)) * 100,
                    2
                ),
            }
        )

    summary_df = pd.DataFrame(outlier_summary)

    worst_column = summary_df.sort_values(
        "Outliers",
        ascending=False
    ).iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Numeric Columns",
            len(numeric_df.columns)
        )

    with col2:
        st.metric(
            "Columns with Outliers",
            (summary_df["Outliers"] > 0).sum()
        )

    with col3:
        st.metric(
            "Worst Column",
            worst_column["Column"]
        )

    st.subheader("📋 Outlier Summary")

    st.dataframe(
        summary_df,
        use_container_width=True
    )

    fig = px.bar(
        summary_df,
        x="Column",
        y="Outliers",
        color="Outliers",
        title="Outliers by Column",
        text="Outliers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("📦 Box Plots")

    selected_column = st.selectbox(
        "Choose Numeric Column",
        numeric_df.columns
    )

    fig2 = px.box(
        df,
        y=selected_column,
        points="outliers",
        title=f"Outliers in {selected_column}"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )