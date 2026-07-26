import streamlit as st

# Components
from components.uploader import upload_dataset

from components.summary_cards import render_summary
from components.quality_cards import render_quality_report

from components.column_explorer import render_column_explorer
from components.charts import render_chart
from components.correlation import render_correlation
from components.missing_values import render_missing_values
from components.outlier_detection import render_outlier_dashboard
from components.data_cleaning import render_data_cleaning
from components.feature_engineering import render_feature_engineering
from components.export_data import render_export

# Services
from services.data_profiler import get_dataset_summary
from services.data_quality import evaluate_data_quality
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="InsightX - Intelligent Data Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 InsightX")
st.subheader("Intelligent Data Analytics Dashboard")

# -----------------------------------------------------------------------------
# Upload Dataset
# -----------------------------------------------------------------------------

df = upload_dataset()

# -----------------------------------------------------------------------------
# Main Dashboard
# -----------------------------------------------------------------------------

if df is not None:

    # Dataset Preview
    st.subheader("📄 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    # Dataset Summary
    summary = get_dataset_summary(df)
    render_summary(summary)

    # Data Quality Report
    quality = evaluate_data_quality(df)
    render_quality_report(quality)

    # Column Explorer
    selected_column = render_column_explorer(df)

    # Interactive Charts
    render_chart(df, selected_column)

    # Correlation Matrix
    render_correlation(df)

    # Missing Value Dashboard
    render_missing_values(df)

    # Outlier Detection
    render_outlier_dashboard(df)

    # Data Cleaning Studio
    df = render_data_cleaning(df)

    # Feature Engineering Studio
    df = render_feature_engineering(df)

    # Export Dataset
    render_export(df)

else:
    st.info("👆 Upload a CSV or Excel file to begin.")