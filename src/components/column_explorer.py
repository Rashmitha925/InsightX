import streamlit as st
import pandas as pd


def render_column_explorer(df: pd.DataFrame):
    """
    Display information about a selected column.
    """

    st.write("## 🔍 Column Explorer")

    selected_column = st.selectbox(
        "Select a column",
        df.columns
    )

    column = df[selected_column]

    st.write(f"### 📌 {selected_column}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Data Type", str(column.dtype))
        st.metric("Missing Values", int(column.isnull().sum()))

    with col2:
        st.metric("Unique Values", int(column.nunique()))
        st.metric("Total Values", len(column))

    st.write("### Sample Values")
    st.dataframe(column.head(10))

    # ----------------------------
    # Numeric Statistics
    # ----------------------------

    if pd.api.types.is_numeric_dtype(column):

        st.write("## 📈 Statistics")

        stats_col1, stats_col2 = st.columns(2)

        with stats_col1:
            st.metric("Mean", round(column.mean(), 2))
            st.metric("Median", round(column.median(), 2))
            st.metric("Minimum", round(column.min(), 2))
            st.metric("25th Percentile", round(column.quantile(0.25), 2))

        with stats_col2:
            st.metric("Maximum", round(column.max(), 2))
            st.metric("Standard Deviation", round(column.std(), 2))
            st.metric("75th Percentile", round(column.quantile(0.75), 2))

    # ----------------------------
    # Categorical Analysis
    # ----------------------------

    else:

        st.write("## 📋 Category Analysis")

        mode_value = column.mode().iloc[0] if not column.mode().empty else "N/A"
        mode_count = column.value_counts().iloc[0] if not column.value_counts().empty else 0

        cat_col1, cat_col2 = st.columns(2)

        with cat_col1:
            st.metric("Most Frequent Value", mode_value)
            st.metric("Number of Categories", int(column.nunique()))

        with cat_col2:
            st.metric("Frequency", int(mode_count))

        st.write("### Top 5 Categories")

        st.dataframe(
            column.value_counts().head(5)
        )