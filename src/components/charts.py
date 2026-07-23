import streamlit as st
import pandas as pd
import plotly.express as px


def render_chart(df: pd.DataFrame, selected_column: str):
    """
    Render interactive charts based on the selected column.
    """

    column = df[selected_column]

    st.write("## 📊 Visual Analytics")

    # ----------------------------
    # Numeric Columns
    # ----------------------------

    if pd.api.types.is_numeric_dtype(column):

        st.write("### 📈 Histogram")

        histogram = px.histogram(
            df,
            x=selected_column,
            nbins=20,
            title=f"Distribution of {selected_column}"
        )

        st.plotly_chart(
            histogram,
            use_container_width=True
        )

        st.write("### 📦 Box Plot")

        boxplot = px.box(
            df,
            y=selected_column,
            title=f"Box Plot of {selected_column}"
        )

        st.plotly_chart(
            boxplot,
            use_container_width=True
        )

    # ----------------------------
    # Categorical Columns
    # ----------------------------

    else:

        counts = (
            column
            .value_counts()
            .head(10)
            .reset_index()
        )

        counts.columns = [
            selected_column,
            "Count"
        ]

        st.write("### 📊 Top Categories")

        bar_chart = px.bar(
            counts,
            x=selected_column,
            y="Count",
            title=f"Top Categories in {selected_column}"
        )

        st.plotly_chart(
            bar_chart,
            use_container_width=True
        )