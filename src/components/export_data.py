import streamlit as st
import pandas as pd
from io import BytesIO


def render_export(cleaned_df: pd.DataFrame):
    """
    Export cleaned dataset as CSV or Excel.
    """

    st.write("# 📤 Export Cleaned Dataset")

    st.info(
        "Download your cleaned dataset in CSV or Excel format."
    )

    # -------------------------
    # CSV Download
    # -------------------------

    csv = cleaned_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

    # -------------------------
    # Excel Download
    # -------------------------

    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        cleaned_df.to_excel(
            writer,
            index=False,
            sheet_name="Cleaned Data"
        )

    st.download_button(
        label="⬇ Download Excel",
        data=excel_buffer.getvalue(),
        file_name="cleaned_dataset.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )