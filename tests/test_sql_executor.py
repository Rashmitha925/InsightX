
import unittest
from datetime import date
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.connection import Base
from src.database.models import SalesRecord
from src.database.query_executor import execute_read_only_query


class TestSQLExecutor(unittest.TestCase):

    def setUp(self):
        # Create an isolated in-memory database
        self.test_engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )

        Base.metadata.create_all(bind=self.test_engine)

        TestSession = sessionmaker(bind=self.test_engine)
        db = TestSession()

        # Insert two temporary sales records
        db.add_all([
            SalesRecord(
                sale_date=date(2026, 1, 5),
                region="South",
                product="Laptop",
                category="Electronics",
                quantity=2,
                unit_price=50000,
                revenue=100000,
                customer_segment="Corporate"
            ),
            SalesRecord(
                sale_date=date(2026, 1, 10),
                region="North",
                product="Monitor",
                category="Electronics",
                quantity=2,
                unit_price=10000,
                revenue=20000,
                customer_segment="Retail"
            )
        ])

        db.commit()
        db.close()

        # Redirect SQL executor to the temporary database
        self.engine_patch = patch(
            "src.database.query_executor.engine",
            self.test_engine
        )

        self.engine_patch.start()

    def tearDown(self):
        self.engine_patch.stop()
        self.test_engine.dispose()

    # 1. Test normal SELECT execution
    def test_select_query(self):
        result = execute_read_only_query(
            "SELECT COUNT(*) AS total FROM sales"
        )

        self.assertEqual(result[0]["total"], 2)

    # 2. Test empty query rejection
    def test_empty_query(self):
        with self.assertRaises(ValueError):
            execute_read_only_query("")

    # 3. Test INSERT rejection
    def test_insert_rejected(self):
        with self.assertRaises(ValueError):
            execute_read_only_query(
                "INSERT INTO sales (region) VALUES ('Test')"
            )

    # 4. Test UPDATE rejection
    def test_update_rejected(self):
        with self.assertRaises(ValueError):
            execute_read_only_query(
                "UPDATE sales SET revenue = 0"
            )

    # 5. Test DELETE rejection
    def test_delete_rejected(self):
        with self.assertRaises(ValueError):
            execute_read_only_query(
                "DELETE FROM sales"
            )

    # 6. Test DROP TABLE rejection
    def test_drop_rejected(self):
        with self.assertRaises(ValueError):
            execute_read_only_query(
                "DROP TABLE sales"
            )

    # 7. Test multiple statement rejection
    def test_multiple_statements_rejected(self):
        with self.assertRaises(ValueError):
            execute_read_only_query(
                "SELECT 1; SELECT 2"
            )

    # 8. Test data integrity
    def test_data_remains_unchanged(self):
        result = execute_read_only_query(
            "SELECT SUM(revenue) AS total_revenue FROM sales"
        )

        self.assertEqual(
            result[0]["total_revenue"],
            120000
        )

    # 9. Test unauthorized system table access
    def test_system_table_access_rejected(self):
        with self.assertRaises(DatabaseError):
            execute_read_only_query(
                "SELECT name FROM sqlite_master"
            )

    # 10. Test unapproved SQL function rejection
    def test_unapproved_function_rejected(self):
        with self.assertRaises(DatabaseError):
            execute_read_only_query(
                "SELECT random() AS value FROM sales"
            )

    # 11. Test approved aggregate functions
    def test_aggregate_function_allowed(self):
        result = execute_read_only_query(
            "SELECT SUM(revenue) AS total FROM sales"
        )

        self.assertEqual(result[0]["total"], 120000)

    # 12. Test maximum result limit
    def test_result_limit(self):
        query = """
        SELECT n
        FROM (
            WITH RECURSIVE numbers(n) AS (
                SELECT 1
                UNION ALL
                SELECT n + 1 FROM numbers WHERE n < 501
            )
            SELECT n FROM numbers
        )
        """

        with self.assertRaises(ValueError):
            execute_read_only_query(query)


if __name__ == "__main__":
    unittest.main()
