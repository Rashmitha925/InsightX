
import streamlit as st

# =============================================================================
# Components
# =============================================================================

from components.uploader import upload_dataset
from components.agent_chat import render_agent_chat

from components.summary_cards import render_summary
from components.quality_cards import render_quality_report

from components.column_explorer import render_column_explorer
from components.charts import render_chart
from components.correlation import render_correlation
from components.missing_values import render_missing_values
from components.outlier_detection import render_outlier_dashboard
from components.data_cleaning import render_data_cleaning
from components.feature_engineering import render_feature_engineering
from components.ai_insights import render_ai_insights
from components.export_data import render_export
from components.statistical_insights import render_statistical_insights
from components.header import render_header
from components.sidebar import render_sidebar
from components.executive_dashboard import render_executive_dashboard
from components.dashboard_overview import render_dashboard_overview

from reports.pdf_generator import generate_pdf_report

# =============================================================================
# Services
# =============================================================================

from services.data_profiler import get_dataset_summary
from services.data_quality import evaluate_data_quality

# =============================================================================
# Page Configuration
# =============================================================================

st.set_page_config(
    page_title="InsightX - Intelligent Data Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

render_sidebar()

# =============================================================================
# Header
# =============================================================================

render_header()

# =============================================================================
# Upload Dataset
# =============================================================================

df = upload_dataset()

# =============================================================================
# Main Dashboard
# =============================================================================

if df is not None:

    # -------------------------------------------------------------------------
    # Dataset Preview
    # -------------------------------------------------------------------------

    render_executive_dashboard(df)
    render_dashboard_overview(df)

    st.subheader("📄 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    # -------------------------------------------------------------------------
    # InsightX Agent Assistant
    # -------------------------------------------------------------------------

    render_agent_chat(df)

    # -------------------------------------------------------------------------
    # Dataset Summary
    # -------------------------------------------------------------------------

    summary = get_dataset_summary(df)
    render_summary(summary)

    # -------------------------------------------------------------------------
    # Data Quality Report
    # -------------------------------------------------------------------------

    quality = evaluate_data_quality(df)
    render_quality_report(quality)

    # -------------------------------------------------------------------------
    # Column Explorer
    # -------------------------------------------------------------------------

    selected_column = render_column_explorer(df)

    # -------------------------------------------------------------------------
    # Interactive Charts
    # -------------------------------------------------------------------------

    render_chart(df, selected_column)

    # -------------------------------------------------------------------------
    # Correlation Analysis
    # -------------------------------------------------------------------------

    render_correlation(df)

    # -------------------------------------------------------------------------
    # Missing Value Dashboard
    # -------------------------------------------------------------------------

    render_missing_values(df)

    # -------------------------------------------------------------------------
    # Outlier Detection
    # -------------------------------------------------------------------------

    render_outlier_dashboard(df)

    # -------------------------------------------------------------------------
    # Statistical Intelligence
    # -------------------------------------------------------------------------

    render_statistical_insights(df)

    # -------------------------------------------------------------------------
    # Data Cleaning Studio
    # -------------------------------------------------------------------------

    cleaned_df = render_data_cleaning(df)

    # -------------------------------------------------------------------------
    # Feature Engineering Studio
    # -------------------------------------------------------------------------

    featured_df = render_feature_engineering(cleaned_df)

    # -------------------------------------------------------------------------
    # AI Insight Generator
    # -------------------------------------------------------------------------

    render_ai_insights(featured_df)

    # -------------------------------------------------------------------------
    # Export Dataset
    # -------------------------------------------------------------------------

    render_export(featured_df)

    # -------------------------------------------------------------------------
    # Executive PDF Report
    # -------------------------------------------------------------------------

    st.markdown("## 📄 Executive PDF Report")

    if st.button("Generate Executive Report"):

        pdf_path = generate_pdf_report(featured_df)

        st.success("✅ Report generated successfully!")

        with open(pdf_path, "rb") as pdf:

            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf,
                file_name="InsightX_Report.pdf",
                mime="application/pdf",
            )
