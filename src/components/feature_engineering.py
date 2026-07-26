import streamlit as st
import pandas as pd

from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler,
    MinMaxScaler
)


def apply_label_encoding(df, columns):

    encoder = LabelEncoder()

    mappings = {}

    for column in columns:

        df[column] = encoder.fit_transform(
            df[column].astype(str)
        )

        mappings[column] = {
            original: encoded
            for encoded, original in enumerate(encoder.classes_)
        }

    return df, mappings


def apply_one_hot_encoding(df, columns):

    return pd.get_dummies(
        df,
        columns=columns
    )


def apply_standard_scaling(df, columns):

    scaler = StandardScaler()

    df[columns] = scaler.fit_transform(df[columns])

    return df


def apply_minmax_scaling(df, columns):

    scaler = MinMaxScaler()

    df[columns] = scaler.fit_transform(df[columns])

    return df


def render_feature_engineering(df):

    st.header("⚙️ Feature Engineering Studio")

    engineered_df = df.copy()

    transformation = st.radio(
        "Select Transformation",
        (
            "Label Encoding",
            "One-Hot Encoding",
            "Standard Scaling",
            "Min-Max Scaling"
        )
    )

    if transformation in (
        "Label Encoding",
        "One-Hot Encoding"
    ):

        columns = engineered_df.select_dtypes(
            include=["object"]
        ).columns.tolist()

    else:

        columns = engineered_df.select_dtypes(
            include=["number"]
        ).columns.tolist()

    if len(columns) == 0:

        st.info(
            "No suitable columns found for this transformation."
        )

        return engineered_df

    selected_columns = st.multiselect(
        "Select Columns",
        columns
    )

    if st.button("🚀 Apply Transformation"):

        if len(selected_columns) == 0:

            st.warning(
                "Please select at least one column."
            )

            return engineered_df

        summary = []

        if transformation == "Label Encoding":

            engineered_df, mappings = apply_label_encoding(
                engineered_df,
                selected_columns
            )

            summary.append(
                f"Label Encoded: {', '.join(selected_columns)}"
            )

            st.subheader("Encoding Mapping")

            for column, mapping in mappings.items():

                st.write(f"**{column}**")

                st.json(mapping)

        elif transformation == "One-Hot Encoding":

            engineered_df = apply_one_hot_encoding(
                engineered_df,
                selected_columns
            )

            summary.append(
                f"One-Hot Encoded: {', '.join(selected_columns)}"
            )

        elif transformation == "Standard Scaling":

            engineered_df = apply_standard_scaling(
                engineered_df,
                selected_columns
            )

            summary.append(
                f"Standard Scaled: {', '.join(selected_columns)}"
            )

        elif transformation == "Min-Max Scaling":

            engineered_df = apply_minmax_scaling(
                engineered_df,
                selected_columns
            )

            summary.append(
                f"Min-Max Scaled: {', '.join(selected_columns)}"
            )

        st.success("Transformation completed successfully.")

        st.subheader("Transformation Summary")

        for item in summary:

            st.success(item)

        st.subheader("Preview")

        st.dataframe(
            engineered_df.head(),
            use_container_width=True
        )

    return engineered_df