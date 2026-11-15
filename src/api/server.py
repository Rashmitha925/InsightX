
from io import BytesIO
from pathlib import Path

import pandas as pd
from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form
)
from pydantic import BaseModel

from src.agent.graph import run_agent
from src.tools.dataset_tool import analyze_dataset


# Create the FastAPI application
app = FastAPI(
    title="InsightX Agent API",
    description="Backend API for the InsightX intelligent analytics agent",
    version="1.0.0"
)


# Define the structure of an incoming question
class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Welcome to InsightX Agent API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Existing endpoint: SQLite-based analytics
@app.post("/ask")
def ask_question(request: QuestionRequest):

    try:
        result = run_agent(request.question)
        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# New endpoint: analytics on uploaded datasets
@app.post("/ask-dataset")
async def ask_dataset_question(
    question: str = Form(""),
    file: UploadFile = File(...)
):

    # Step 1: Validate the uploaded file extension
    file_extension = Path(file.filename or "").suffix.lower()

    if file_extension not in [".csv", ".xlsx"]:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel (.xlsx) files are supported."
        )

    try:
        # Step 2: Read the uploaded file
        file_content = await file.read()

        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        # Step 3: Convert the uploaded file into a DataFrame
        if file_extension == ".csv":
            df = pd.read_csv(BytesIO(file_content))
        else:
            df = pd.read_excel(BytesIO(file_content))

        # Step 4: Validate the dataset
        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="The uploaded dataset contains no data."
            )

        # Step 5: Analyze the user's question
        result = analyze_dataset(question, df)

        # Step 6: Return the result
        return {
            "filename": file.filename,
            "question": question,
            "selected_tool": "dataset_analytics",
            "tool_result": result["result"],
            "operation": result["operation"],
            "final_answer": result["answer"]
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unable to read the uploaded file. "
                "Please check that it is a valid CSV or Excel file."
            )
        )

    finally:
        await file.close()
