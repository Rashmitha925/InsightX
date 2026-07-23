import streamlit as st

from components.header import render_header
from components.uploader import upload_dataset
from components.summary_cards import render_summary
from components.quality_cards import render_quality_report
from components.column_explorer import render_column_explorer

from services.data_profiler import get_dataset_summary
from services.data_quality import evaluate_data_quality


st.set_page_config(
    page_title="InsightX",
    page_icon="📊",
    layout="wide"
)

render_header()

df = upload_dataset()

if df is not None:

    # Dataset Preview
    st.write("## 📄 Dataset Preview")
    st.dataframe(df.head())

    # Dataset Summary
    summary = get_dataset_summary(df)
    render_summary(summary)

    # Data Quality
    quality = evaluate_data_quality(df)
    render_quality_report(quality)

    # Column Explorer
    render_column_explorer(df)