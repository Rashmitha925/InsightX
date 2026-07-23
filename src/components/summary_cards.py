import streamlit as st


def render_summary(summary: dict):
    """
    Display dataset summary cards.
    """

    st.write("## 📊 Dataset Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", summary["Rows"])
        st.metric("Columns", summary["Columns"])
        st.metric("Missing Values", summary["Missing Values"])

    with col2:
        st.metric("Duplicate Rows", summary["Duplicate Rows"])
        st.metric("Memory Usage (KB)", summary["Memory Usage (KB)"])