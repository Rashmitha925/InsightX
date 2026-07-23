import streamlit as st
import pandas as pd


def render_data_cleaning(df: pd.DataFrame):
    """
    Data Cleaning Studio
    """

    st.write("# 🧹 Data Cleaning Studio")

    cleaned_df = df.copy()

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

    missing_columns = cleaned_df.columns[
        cleaned_df.isnull().any()
    ].tolist()

    if len(missing_columns) == 0:

        st.success("✅ No missing values found.")

    else:

        selected_column = st.selectbox(
            "Select Column",
            missing_columns
        )

        strategy = st.selectbox(
            "Fill Using",
            [
                "Mean",
                "Median",
                "Mode"
            ]
        )

        if st.button("Apply Missing Value Treatment"):

            if strategy == "Mean":

                cleaned_df[selected_column] = cleaned_df[selected_column].fillna(
                    cleaned_df[selected_column].mean()
                )

            elif strategy == "Median":

                cleaned_df[selected_column] = cleaned_df[selected_column].fillna(
                    cleaned_df[selected_column].median()
                )

            else:

                cleaned_df[selected_column] = cleaned_df[selected_column].fillna(
                    cleaned_df[selected_column].mode()[0]
                )

            st.success(
                f"✅ Missing values filled using {strategy}."
            )

    return cleaned_df