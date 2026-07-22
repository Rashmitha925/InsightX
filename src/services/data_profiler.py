import pandas as pd


def get_dataset_summary(df: pd.DataFrame) -> dict:
    """
    Generate a summary of the uploaded dataset.
    """

    summary = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Memory Usage (KB)": round(df.memory_usage(deep=True).sum() / 1024, 2),
        "Column Names": list(df.columns),
        "Data Types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        }
    }

    return summary