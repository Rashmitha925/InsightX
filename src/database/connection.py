
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Load environment variables from the .env file
load_dotenv()

# Read the database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./insightx.db"
)

# Configure SQLite connections
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

# Create a session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for future database models
Base = declarative_base()


# Provide a database session
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
