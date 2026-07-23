import pandas as pd


def evaluate_data_quality(df: pd.DataFrame) -> dict:
    """
    Evaluate the quality of the uploaded dataset.
    """

    score = 100

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    if df.shape[0] == 0:
        score = 0

    if missing_values > 0:
        score -= 10

    if duplicate_rows > 0:
        score -= 10

    score = max(0, min(score, 100))

    numeric_columns = len(
        df.select_dtypes(include="number").columns
    )

    categorical_columns = len(
        df.select_dtypes(include="object").columns
    )

    if score >= 90:
        quality = "Excellent"
    elif score >= 70:
        quality = "Good"
    elif score >= 50:
        quality = "Needs Attention"
    else:
        quality = "Poor"

    return {
        "Score": score,
        "Quality": quality,
        "Missing Values": missing_values,
        "Duplicate Rows": duplicate_rows,
        "Numeric Columns": numeric_columns,
        "Categorical Columns": categorical_columns
    }