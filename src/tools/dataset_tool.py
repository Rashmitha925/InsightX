
import re
import pandas as pd


def find_matching_numeric_column(
    question: str,
    numeric_columns: list
):
    """
    Match a complete numeric column name in the question.
    """

    for column in numeric_columns:
        column_name = str(column).lower().strip()

        pattern = (
            r"(?<!\w)"
            + re.escape(column_name)
            + r"(?!\w)"
        )

        if re.search(pattern, question):
            return column

    return None


def analyze_dataset(question: str, df: pd.DataFrame) -> dict:
    """
    Analyze an uploaded DataFrame using supported operations.
    """

    # Step 1: Validate the question and dataset
    if not question or not question.strip():
        raise ValueError("Please enter a valid question.")

    if df is None or df.empty:
        raise ValueError("The uploaded dataset is empty.")

    question = question.lower().strip()

    # Step 2: Answer dataset row count
    if "row" in question:
        result = len(df)

        return {
            "operation": "row_count",
            "result": result,
            "answer": f"The dataset contains {result:,} rows."
        }

    # Step 3: Answer dataset column count
    if "how many columns" in question or "column count" in question:
        result = len(df.columns)

        return {
            "operation": "column_count",
            "result": result,
            "answer": f"The dataset contains {result:,} columns."
        }

    # Step 4: Return dataset column names
    if "column" in question and any(
        word in question
        for word in ["which", "list", "name", "show"]
    ):
        result = df.columns.tolist()

        return {
            "operation": "column_names",
            "result": result,
            "answer": "Dataset columns: "
            + ", ".join(map(str, result))
        }

    # Step 5: Calculate missing values
    if "missing" in question or "null" in question:
        result = int(df.isnull().sum().sum())

        return {
            "operation": "missing_values",
            "result": result,
            "answer": (
                f"The dataset contains {result:,} "
                f"{'missing value' if result == 1 else 'missing values'}."
            )
        }

    # Step 6: Identify numeric columns
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # Step 7: Calculate average of a numeric column
    if "average" in question or "mean" in question:

        matching_column = find_matching_numeric_column(
            question,
            numeric_columns
        )

        if matching_column is None:
            raise ValueError(
                "Please mention a valid numeric column "
                "for the average calculation."
            )

        result = float(df[matching_column].mean())

        return {
            "operation": "column_average",
            "column": matching_column,
            "result": result,
            "answer": (
                f"The average of {matching_column} "
                f"is {result:,.2f}."
            )
        }

    # Step 8: Calculate maximum of a numeric column
    if any(
        word in question
        for word in ["highest", "maximum", "max"]
    ):

        matching_column = find_matching_numeric_column(
            question,
            numeric_columns
        )

        if matching_column is None:
            raise ValueError(
                "Please mention a valid numeric column "
                "for the maximum calculation."
            )

        result = float(df[matching_column].max())

        return {
            "operation": "column_maximum",
            "column": matching_column,
            "result": result,
            "answer": (
                f"The highest value in {matching_column} "
                f"is {result:,.2f}."
            )
        }

    # Step 9: Handle unsupported questions
    return {
        "operation": "unsupported",
        "result": None,
        "answer": (
            "This question is not supported yet. "
            "Try asking about row count, column count, "
            "column names, missing values, average, "
            "or highest numeric value."
        )
    }
