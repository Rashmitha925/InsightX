
import unittest
from unittest.mock import patch

from src.agent.graph import run_agent


class TestAgentWorkflow(unittest.TestCase):

    # Test SQL question routing
    def test_sql_routing(self):
        result = run_agent("Calculate average revenue")
        self.assertEqual(result["selected_tool"], "sql")

    # Test document question routing
    def test_rag_routing(self):
        result = run_agent("Find information in this PDF report")
        self.assertEqual(result["selected_tool"], "rag")

    # Test chart question routing
    def test_chart_routing(self):
        result = run_agent("Show monthly sales trend in a chart")
        self.assertEqual(result["selected_tool"], "sql_chart")

    # Test general question routing
    def test_general_question(self):
        result = run_agent("Hello, how are you?")
        self.assertEqual(result["selected_tool"], "answer")

    # Test removal of unnecessary spaces
    def test_question_whitespace(self):
        result = run_agent("   Calculate average revenue   ")
        self.assertEqual(
            result["user_question"],
            "Calculate average revenue"
        )

    # Test rejection of empty questions
    def test_empty_question(self):
        with self.assertRaises(ValueError):
            run_agent("")

    # Test rejection of whitespace-only questions
    def test_spaces_only_question(self):
        with self.assertRaises(ValueError):
            run_agent("   ")

    # Test total revenue SQL execution
    @patch("src.agent.graph.run_sql_tool")
    def test_total_revenue_execution(self, mock_sql_tool):

        mock_sql_tool.return_value = [
            {"total_revenue": 2067000.0}
        ]

        result = run_agent("What is the total revenue?")

        mock_sql_tool.assert_called_once_with("total_revenue")

        self.assertEqual(
            result["tool_result"],
            [{"total_revenue": 2067000.0}]
        )

        self.assertIn(
            "₹2,067,000.00",
            result["final_answer"]
        )

    # Test total sales SQL execution
    @patch("src.agent.graph.run_sql_tool")
    def test_total_sales_execution(self, mock_sql_tool):

        mock_sql_tool.return_value = [
            {"total_records": 15}
        ]

        result = run_agent("How many sales records are there?")

        mock_sql_tool.assert_called_once_with("total_sales")

        self.assertIn(
            "15 sales records",
            result["final_answer"]
        )

    # Test revenue by region SQL execution
    @patch("src.agent.graph.run_sql_tool")
    def test_revenue_by_region_execution(self, mock_sql_tool):

        mock_sql_tool.return_value = [
            {"region": "West", "total_revenue": 854000.0},
            {"region": "South", "total_revenue": 660000.0},
            {"region": "North", "total_revenue": 553000.0}
        ]

        result = run_agent("Show revenue by region")

        mock_sql_tool.assert_called_once_with(
            "revenue_by_region"
        )

        self.assertIn("West", result["final_answer"])
        self.assertIn("South", result["final_answer"])
        self.assertIn("North", result["final_answer"])

    # Test unsupported average revenue question
    @patch("src.agent.graph.run_sql_tool")
    def test_unsupported_average_revenue(self, mock_sql_tool):

        result = run_agent("Calculate average revenue")

        mock_sql_tool.assert_not_called()

        self.assertIsNone(result["tool_result"])

        self.assertIn(
            "not supported yet",
            result["final_answer"]
        )


if __name__ == "__main__":
    unittest.main()
