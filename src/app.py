import streamlit as st

from components.header import render_header
from components.uploader import upload_dataset
from components.summary_cards import render_summary
from components.quality_cards import render_quality_report
from services.data_quality import evaluate_data_quality
from components.column_explorer import render_column_explorer
from components.charts import render_chart
from components.correlation import render_correlation
from components.missing_values import render_missing_values
from components.outlier_detection import render_outlier_dashboard
from services.data_profiler import get_dataset_summary
from components.data_cleaning import render_data_cleaning


st.set_page_config(
    page_title="InsightX",
    page_icon="📊",
    layout="wide"
)

render_header()

df = upload_dataset()

if df is not None:

    st.subheader("📄 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    summary = get_dataset_summary(df)
    render_summary(summary)

    quality = evaluate_data_quality(df)
    render_quality_report(quality)

    selected_column = render_column_explorer(df)

    render_chart(df, selected_column)

    render_correlation(df)

    render_missing_values(df)

    render_outlier_dashboard(df)
    cleaned_df = render_data_cleaning(df)