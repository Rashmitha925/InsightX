import streamlit as st
import pandas as pd


def render_statistical_insights(df: pd.DataFrame):
    """
    Statistical Intelligence Dashboard
    """

    st.divider()

    st.header("📊 Statistical Intelligence")

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        st.info("No numeric columns available.")
        return

    stats = numeric_df.describe().T

    stats["Range"] = stats["max"] - stats["min"]

    highest_mean = stats["mean"].idxmax()
    lowest_mean = stats["mean"].idxmin()

    highest_variance = numeric_df.var().idxmax()
    highest_std = stats["std"].idxmax()

    largest_range = stats["Range"].idxmax()

    most_stable = stats["std"].idxmin()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Highest Mean",
            highest_mean,
            f"{stats.loc[highest_mean,'mean']:.2f}"
        )

    with col2:
        st.metric(
            "Highest Variance",
            highest_variance,
            f"{numeric_df.var()[highest_variance]:.2f}"
        )

    with col3:
        st.metric(
            "Largest Range",
            largest_range,
            f"{stats.loc[largest_range,'Range']:.2f}"
        )

    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            "Lowest Mean",
            lowest_mean,
            f"{stats.loc[lowest_mean,'mean']:.2f}"
        )

    with col5:
        st.metric(
            "Most Stable Feature",
            most_stable,
            f"{stats.loc[most_stable,'std']:.2f}"
        )

    st.subheader("📋 Complete Statistical Summary")

    st.dataframe(
        stats[
            [
                "mean",
                "std",
                "min",
                "25%",
                "50%",
                "75%",
                "max",
                "Range"
            ]
        ].round(2),
        use_container_width=True
    )