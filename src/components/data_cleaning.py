import streamlit as st
import pandas as pd


def render_data_cleaning(df: pd.DataFrame):
    """
    Data Cleaning Studio
    """

    st.write("# 🧹 Data Cleaning Studio")

    # ==========================================================
    # Store cleaned dataframe in Session State
    # ==========================================================

    if "cleaned_df" not in st.session_state:
        st.session_state.cleaned_df = df.copy()

    cleaned_df = st.session_state.cleaned_df

    st.info("Choose the cleaning operations you want to perform.")

    # ==========================================================
    # Remove Duplicate Rows
    # ==========================================================

    st.write("## 🗑️ Remove Duplicate Rows")

    duplicate_rows = cleaned_df.duplicated().sum()

    st.metric(
        "Duplicate Rows Found",
        int(duplicate_rows)
    )

    remove_duplicates = st.checkbox("Remove duplicate rows")

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

       # ==========================================================
    # Missing Value Treatment
    # ==========================================================

    st.write("## 🩹 Missing Value Treatment")

    total_missing = cleaned_df.isnull().sum().sum()

    st.metric(
        "Total Missing Values",
        int(total_missing)
    )

    if total_missing == 0:

        st.success("✅ No missing values found.")

    else:

        st.info(
            "Click the button below to automatically fill all missing values."
        )

        if st.button("🚀 Auto Clean Missing Values"):

            # Fill numeric columns with median
            numeric_columns = cleaned_df.select_dtypes(
                include=["number"]
            ).columns

            for column in numeric_columns:

                cleaned_df[column] = cleaned_df[column].fillna(
                    cleaned_df[column].median()
                )

            # Fill categorical columns with mode
            categorical_columns = cleaned_df.select_dtypes(
                exclude=["number"]
            ).columns

            for column in categorical_columns:

                if not cleaned_df[column].mode().empty:

                    cleaned_df[column] = cleaned_df[column].fillna(
                        cleaned_df[column].mode()[0]
                    )

            remaining_missing = cleaned_df.isnull().sum().sum()

            st.success(
                f"✅ Missing value treatment completed.\n\nRemaining Missing Values: {remaining_missing}"
            )
    return cleaned_df