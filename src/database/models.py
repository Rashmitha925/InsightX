
from sqlalchemy import Column, Integer, String, Float, Date

from src.database.connection import Base


class SalesRecord(Base):

    # Name of the database table
    __tablename__ = "sales"

    # Unique identifier for every sales record
    id = Column(Integer, primary_key=True, index=True)

    # Date of the sale
    sale_date = Column(Date, nullable=False)

    # Business information
    region = Column(String(100), nullable=False)
    product = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)

    # Sales information
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    revenue = Column(Float, nullable=False)

    # Customer information
    customer_segment = Column(String(100), nullable=False)
