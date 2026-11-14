
from src.database.connection import engine, Base

# Import models so SQLAlchemy knows which tables to create
from src.database.models import SalesRecord


def initialize_database():
    # Create all tables defined in the models
    Base.metadata.create_all(bind=engine)

    print("Database initialized successfully.")
    print("Created tables:", list(Base.metadata.tables.keys()))


if __name__ == "__main__":
    initialize_database()
