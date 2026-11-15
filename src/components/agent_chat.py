
import streamlit as st
import requests


def render_agent_chat(df):
    """
    Display the InsightX Agent chat interface
    and send dataset questions to the FastAPI backend.
    """

    st.markdown("---")
    st.subheader("🤖 Ask InsightX Agent")

    st.caption(
        "Ask questions about your uploaded dataset "
        "using natural language."
    )

    # API address for local development
    api_url = "http://127.0.0.1:8000/ask-dataset"

    # Input field for the user's question
    question = st.text_input(
        "Enter your question",
        placeholder="Example: What is the average Salary?"
    )

    # Submit question to the backend
    if st.button("Ask InsightX", key="ask_dataset_button"):

        if not question.strip():
            st.warning("Please enter a question.")

        elif df is None or df.empty:
            st.warning("Please upload a valid dataset first.")

        else:
            try:
                # Convert the DataFrame into CSV bytes
                csv_data = df.to_csv(index=False).encode("utf-8")

                files = {
                    "file": (
                        "uploaded_dataset.csv",
                        csv_data,
                        "text/csv"
                    )
                }

                data = {
                    "question": question
                }

                # Send the question and dataset to FastAPI
                with st.spinner("Analyzing your dataset..."):

                    response = requests.post(
                        api_url,
                        data=data,
                        files=files,
                        timeout=30
                    )

                # Handle the backend response
                if response.status_code == 200:

                    result = response.json()

                    st.success("Analysis completed!")

                    st.markdown("### Agent Response")

                    st.write(result["final_answer"])

                    with st.expander("View technical details"):
                        st.write("Selected tool:", result["selected_tool"])
                        st.write("Operation:", result["operation"])
                        st.write("Result:", result["tool_result"])

                else:
                    try:
                        error_detail = response.json().get(
                            "detail",
                            "The API returned an error."
                        )
                    except ValueError:
                        error_detail = "The API returned an invalid response."

                    st.error(f"API Error: {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Unable to connect to the InsightX Agent API. "
                    "Please make sure the FastAPI server is running."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The request took too long. Please try again."
                )

            except requests.exceptions.RequestException as error:
                st.error(f"Request failed: {error}")
