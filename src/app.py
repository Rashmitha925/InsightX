import streamlit as st

from components.header import render_header
from components.uploader import upload_dataset
from components.summary_cards import render_summary
from components.quality_cards import render_quality_report
from components.column_explorer import render_column_explorer
from components.charts import render_chart
from components.correlation import render_correlation
from components.missing_values import render_missing_values
from components.outlier_detection import render_outlier_dashboard
from components.data_cleaning import render_data_cleaning
from components.export_data import render_export

from services.data_profiler import get_dataset_summary
from services.data_quality import evaluate_data_quality


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="InsightX",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------

render_header()

# --------------------------------------------------
# Upload Dataset
# --------------------------------------------------

df = upload_dataset()

# --------------------------------------------------
# Main Dashboard
# --------------------------------------------------

if df is not None:

    # Dataset Preview
    st.subheader("📄 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    # Dataset Summary
    summary = get_dataset_summary(df)
    render_summary(summary)

    # Data Quality
    quality = evaluate_data_quality(df)
    render_quality_report(quality)

    # Column Explorer
    selected_column = render_column_explorer(df)

    # Charts
    render_chart(df, selected_column)

    # Correlation Matrix
    render_correlation(df)

    # Missing Value Dashboard
    render_missing_values(df)

    # Outlier Detection
    render_outlier_dashboard(df)

    # Data Cleaning Studio
    df = render_data_cleaning(df)

    # Export Cleaned Dataset
    render_export(df)