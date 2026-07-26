from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER
title_style.textColor = colors.HexColor("#0F62FE")

subtitle_style = styles["Heading2"]
subtitle_style.alignment = TA_CENTER
subtitle_style.textColor = colors.HexColor("#4F4F4F")

heading_style = styles["Heading2"]
heading_style.textColor = colors.HexColor("#0F62FE")

normal_style = styles["BodyText"]


def create_cover(story):
    story.append(Paragraph("<b>InsightX</b>", title_style))
    story.append(Paragraph("Enterprise Data Analytics Platform", subtitle_style))
    story.append(Spacer(1, 0.35 * inch))


def create_summary_table(story, df):
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Spacer(1, 0.15 * inch))

    numeric_cols = len(df.select_dtypes(include="number").columns)
    categorical_cols = len(df.select_dtypes(exclude="number").columns)

    table_data = [
        ["Metric", "Value"],
        ["Total Rows", str(df.shape[0])],
        ["Total Columns", str(df.shape[1])],
        ["Numeric Columns", str(numeric_cols)],
        ["Categorical Columns", str(categorical_cols)],
        ["Missing Values", str(df.isnull().sum().sum())],
        ["Duplicate Rows", str(df.duplicated().sum())],
    ]

    table = Table(table_data, colWidths=[3.5 * inch, 2 * inch])

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F62FE")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ]
        )
    )

    story.append(table)
    story.append(Spacer(1, 0.3 * inch))
def create_data_quality(story, df):
    story.append(Paragraph("Data Quality Assessment", heading_style))
    story.append(Spacer(1, 0.15 * inch))

    total_cells = df.shape[0] * df.shape[1]

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    missing_percent = (
        (missing_values / total_cells) * 100 if total_cells > 0 else 0
    )

    duplicate_percent = (
        (duplicate_rows / len(df)) * 100 if len(df) > 0 else 0
    )

    if missing_percent < 5 and duplicate_percent == 0:
        quality = "Excellent"
    elif missing_percent < 10:
        quality = "Good"
    else:
        quality = "Needs Improvement"

    quality_table = [
        ["Metric", "Value"],
        ["Overall Quality", quality],
        ["Missing Data (%)", f"{missing_percent:.2f}%"],
        ["Duplicate Rows (%)", f"{duplicate_percent:.2f}%"],
    ]

    table = Table(quality_table, colWidths=[3.5 * inch, 2 * inch])

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F62FE")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("TOPPADDING", (0, 1), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ])
    )

    story.append(table)
    story.append(Spacer(1, 0.30 * inch))


def create_ai_insights(story, df):
    story.append(Paragraph("AI Insights", heading_style))
    story.append(Spacer(1, 0.15 * inch))

    numeric_cols = len(df.select_dtypes(include="number").columns)
    categorical_cols = len(df.select_dtypes(exclude="number").columns)

    insights = [
        f"• Dataset contains <b>{len(df)}</b> records and <b>{df.shape[1]}</b> features.",
        f"• Numeric Columns: <b>{numeric_cols}</b>, Categorical Columns: <b>{categorical_cols}</b>.",
        f"• Missing Values detected: <b>{int(df.isnull().sum().sum())}</b>.",
        f"• Duplicate Rows detected: <b>{int(df.duplicated().sum())}</b>.",
    ]

    if df.isnull().sum().sum() == 0:
        insights.append("• Dataset is complete with no missing values.")

    if df.duplicated().sum() == 0:
        insights.append("• No duplicate records detected.")

    for item in insights:
        story.append(Paragraph(item, normal_style))

    story.append(Spacer(1, 0.30 * inch))


def create_recommendations(story, df):
    story.append(Paragraph("Recommendations", heading_style))
    story.append(Spacer(1, 0.15 * inch))

    recommendations = []

    if df.isnull().sum().sum() > 0:
        recommendations.append(
            "• Handle remaining missing values before building predictive models."
        )

    if len(df.select_dtypes(exclude="number").columns) > 0:
        recommendations.append(
            "• Encode categorical variables before machine learning."
        )

    recommendations.append(
        "• Scale numerical features where required."
    )

    recommendations.append(
        "• Perform feature selection for improved model performance."
    )

    recommendations.append(
        "• Validate the dataset before deployment."
    )

    for rec in recommendations:
        story.append(Paragraph(rec, normal_style))

    story.append(Spacer(1, 0.35 * inch))


def create_footer(story):
    footer = """
    <para align='center'>
    <b>Generated by InsightX</b><br/>
    Enterprise Data Analytics Platform<br/>
    Version 1.0
    </para>
    """

    story.append(Paragraph(footer, normal_style))


def generate_pdf_report(df, filename="InsightX_Report.pdf"):
    doc = SimpleDocTemplate(filename)

    story = []

    create_cover(story)
    create_summary_table(story, df)
    create_data_quality(story, df)
    create_ai_insights(story, df)
    create_recommendations(story, df)
    create_footer(story)

    doc.build(story)

    return filename