
import unittest
from unittest.mock import patch

from src.tools.sql_tool import run_sql_tool


class TestSQLTool(unittest.TestCase):

    # Test total revenue query
    @patch("src.tools.sql_tool.execute_read_only_query")
    def test_total_revenue_query(self, mock_executor):

        mock_executor.return_value = [
            {"total_revenue": 2067000.0}
        ]

        result = run_sql_tool("total_revenue")

        self.assertEqual(
            result[0]["total_revenue"],
            2067000.0
        )

        mock_executor.assert_called_once()

    # Test total sales query
    @patch("src.tools.sql_tool.execute_read_only_query")
    def test_total_sales_query(self, mock_executor):

        mock_executor.return_value = [
            {"total_records": 15}
        ]

        result = run_sql_tool("total_sales")

        self.assertEqual(
            result[0]["total_records"],
            15
        )

        mock_executor.assert_called_once()

    # Test revenue by region query
    @patch("src.tools.sql_tool.execute_read_only_query")
    def test_revenue_by_region_query(self, mock_executor):

        mock_executor.return_value = [
            {"region": "West", "total_revenue": 854000.0},
            {"region": "South", "total_revenue": 660000.0},
            {"region": "North", "total_revenue": 553000.0}
        ]

        result = run_sql_tool("revenue_by_region")

        self.assertEqual(len(result), 3)

        mock_executor.assert_called_once()

    # Test unsupported query type
    @patch("src.tools.sql_tool.execute_read_only_query")
    def test_unsupported_query(self, mock_executor):

        with self.assertRaises(ValueError):
            run_sql_tool("unknown_query")

        mock_executor.assert_not_called()


if __name__ == "__main__":
    unittest.main()
