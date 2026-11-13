
from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(
    title="InsightX Agent API",
    description="Backend API for the InsightX intelligent analytics agent",
    version="1.0.0"
)


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
