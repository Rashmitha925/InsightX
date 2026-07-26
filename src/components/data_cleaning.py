import streamlit as st
import pandas as pd


def render_data_cleaning(df: pd.DataFrame):
    """
    Data Cleaning Studio
    """

    st.header("🧹 Data Cleaning Studio")

    # ---------------------------------------------------------
    # Store cleaned dataframe
    # ---------------------------------------------------------

    if "cleaned_df" not in st.session_state:
        st.session_state.cleaned_df = df.copy()

    cleaned_df = st.session_state.cleaned_df

    st.info("Choose the cleaning operations you want to perform.")

    # =========================================================
    # Remove Duplicate Rows
    # =========================================================

    st.subheader("🗑 Remove Duplicate Rows")

    duplicate_rows = int(cleaned_df.duplicated().sum())

    st.metric(
        "Duplicate Rows Found",
        duplicate_rows
    )

    remove_duplicates = st.checkbox(
        "Remove duplicate rows",
        key="remove_duplicates_checkbox"
    )

    if remove_duplicates:

        cleaned_df = cleaned_df.drop_duplicates()

        st.session_state.cleaned_df = cleaned_df

        st.success(
            f"✅ Removed {duplicate_rows} duplicate rows."
        )

        st.metric(
            "Remaining Rows",
            len(cleaned_df)
        )

    # =========================================================
    # Missing Value Treatment
    # =========================================================

    st.subheader("🩹 Missing Value Treatment")

    total_missing = int(cleaned_df.isnull().sum().sum())

    st.metric(
        "Total Missing Values",
        total_missing
    )

    if total_missing == 0:

        st.success("✅ No missing values found.")

    else:

        method = st.selectbox(
            "Select Missing Value Treatment",
            [
                "Mean",
                "Median",
                "Mode"
            ],
            key="missing_value_method"
        )

        numeric_columns = cleaned_df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        if method in ["Mean", "Median"]:
            available_columns = numeric_columns
        else:
            available_columns = cleaned_df.columns.tolist()

        selected_columns = st.multiselect(
            "Select Columns",
            available_columns,
            key="missing_value_columns"
        )

        if st.button(
            "🚀 Apply Cleaning",
            key="apply_missing_value_treatment"
        ):

            if len(selected_columns) == 0:

                st.warning(
                    "Please select at least one column."
                )

            else:

                for column in selected_columns:

                    if method == "Mean":

                        cleaned_df[column] = cleaned_df[column].fillna(
                            cleaned_df[column].mean()
                        )

                    elif method == "Median":

                        cleaned_df[column] = cleaned_df[column].fillna(
                            cleaned_df[column].median()
                        )

                    elif method == "Mode":

                        mode = cleaned_df[column].mode()

                        if not mode.empty:

                            cleaned_df[column] = cleaned_df[column].fillna(
                                mode[0]
                            )

                st.session_state.cleaned_df = cleaned_df

                remaining_missing = int(
                    cleaned_df.isnull().sum().sum()
                )

                st.success(
                    f"✅ Missing value treatment completed successfully.\n\nRemaining Missing Values: {remaining_missing}"
                )

    return cleaned_df