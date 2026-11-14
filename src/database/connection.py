
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool


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

    # Avoid reusing SQLite connections.
    # This prevents security callbacks from affecting
    # future database operations.
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        poolclass=NullPool
    )

else:
    # Use normal connection pooling for other databases
    engine = create_engine(
        DATABASE_URL,
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
