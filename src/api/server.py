
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.agent.graph import run_agent


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


@app.post("/ask")
def ask_question(request: QuestionRequest):

    try:
        # Send the question to the agent workflow
        result = run_agent(request.question)

        # Return the agent's response
        return result

    except ValueError as error:
        # Handle invalid questions
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
