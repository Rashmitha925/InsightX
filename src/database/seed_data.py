
from datetime import date

from src.database.connection import SessionLocal
from src.database.models import SalesRecord


def seed_database():

    db = SessionLocal()

    try:
        # Avoid inserting duplicate sample records
        existing_records = db.query(SalesRecord).count()

        if existing_records > 0:
            print("Sales data already exists.")
            print("Existing records:", existing_records)
            return

        # Sample business sales records
        sales_records = [
            SalesRecord(
                sale_date=date(2026, 1, 5),
                region="South",
                product="Laptop",
                category="Electronics",
                quantity=5,
                unit_price=50000,
                revenue=250000,
                customer_segment="Corporate"
            ),
            SalesRecord(
                sale_date=date(2026, 1, 12),
                region="North",
                product="Smartphone",
                category="Electronics",
                quantity=10,
                unit_price=20000,
                revenue=200000,
                customer_segment="Retail"
            ),
            SalesRecord(
                sale_date=date(2026, 1, 18),
                region="West",
                product="Office Chair",
                category="Furniture",
                quantity=8,
                unit_price=5000,
                revenue=40000,
                customer_segment="Corporate"
            ),
            SalesRecord(
                sale_date=date(2026, 1, 22),
                region="South",
                product="Monitor",
                category="Electronics",
                quantity=6,
                unit_price=12000,
                revenue=72000,
                customer_segment="Small Business"
            ),
            SalesRecord(
                sale_date=date(2026, 1, 28),
                region="North",
                product="Desk",
                category="Furniture",
                quantity=4,
                unit_price=8000,
                revenue=32000,
                customer_segment="Retail"
            ),
            SalesRecord(
                sale_date=date(2026, 2, 3),
                region="West",
                product="Laptop",
                category="Electronics",
                quantity=7,
                unit_price=50000,
                revenue=350000,
                customer_segment="Corporate"
            ),
            SalesRecord(
                sale_date=date(2026, 2, 8),
                region="South",
                product="Smartphone",
                category="Electronics",
                quantity=12,
                unit_price=20000,
                revenue=240000,
                customer_segment="Retail"
            ),
            SalesRecord(
                sale_date=date(2026, 2, 14),
                region="North",
                product="Office Chair",
                category="Furniture",
                quantity=5,
                unit_price=5000,
                revenue=25000,
                customer_segment="Small Business"
            ),
            SalesRecord(
                sale_date=date(2026, 2, 19),
                region="West",
                product="Monitor",
                category="Electronics",
                quantity=9,
                unit_price=12000,
                revenue=108000,
                customer_segment="Corporate"
            ),
            SalesRecord(
                sale_date=date(2026, 2, 25),
                region="South",
                product="Desk",
                category="Furniture",
                quantity=6,
                unit_price=8000,
                revenue=48000,
                customer_segment="Retail"
            ),
            SalesRecord(
                sale_date=date(2026, 3, 4),
                region="North",
                product="Laptop",
                category="Electronics",
                quantity=4,
                unit_price=50000,
                revenue=200000,
                customer_segment="Corporate"
            ),
            SalesRecord(
                sale_date=date(2026, 3, 10),
                region="West",
                product="Smartphone",
                category="Electronics",
                quantity=15,
                unit_price=20000,
                revenue=300000,
                customer_segment="Retail"
            ),
            SalesRecord(
                sale_date=date(2026, 3, 16),
                region="South",
                product="Office Chair",
                category="Furniture",
                quantity=10,
                unit_price=5000,
                revenue=50000,
                customer_segment="Small Business"
            ),
            SalesRecord(
                sale_date=date(2026, 3, 22),
                region="North",
                product="Monitor",
                category="Electronics",
                quantity=8,
                unit_price=12000,
                revenue=96000,
                customer_segment="Corporate"
            ),
            SalesRecord(
                sale_date=date(2026, 3, 28),
                region="West",
                product="Desk",
                category="Furniture",
                quantity=7,
                unit_price=8000,
                revenue=56000,
                customer_segment="Retail"
            )
        ]

        # Insert all records into the database
        db.add_all(sales_records)

        # Save changes
        db.commit()

        print("Sample sales data inserted successfully.")
        print("Records inserted:", len(sales_records))

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
