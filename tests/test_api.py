
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.api.server import app


class TestInsightXAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    # Test the home endpoint
    def test_home_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            "running"
        )

    # Test the health endpoint
    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            "healthy"
        )

    # Test successful question submission
    @patch("src.api.server.run_agent")
    def test_ask_endpoint(self, mock_run_agent):

        mock_run_agent.return_value = {
            "user_question": "What is the total revenue?",
            "selected_tool": "sql",
            "tool_result": [
                {"total_revenue": 2067000.0}
            ],
            "final_answer": "The total revenue is ₹2,067,000.00."
        }

        response = self.client.post(
            "/ask",
            json={
                "question": "What is the total revenue?"
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json()["selected_tool"],
            "sql"
        )

        self.assertEqual(
            response.json()["tool_result"][0]["total_revenue"],
            2067000.0
        )

        mock_run_agent.assert_called_once_with(
            "What is the total revenue?"
        )

    # Test unsupported question response
    @patch("src.api.server.run_agent")
    def test_unsupported_question(self, mock_run_agent):

        mock_run_agent.return_value = {
            "user_question": "Calculate average revenue",
            "selected_tool": "sql",
            "tool_result": None,
            "final_answer": "This SQL operation is not supported yet."
        }

        response = self.client.post(
            "/ask",
            json={
                "question": "Calculate average revenue"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()["tool_result"])

    # Test empty question validation
    def test_empty_question(self):

        response = self.client.post(
            "/ask",
            json={"question": ""}
        )

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.json()["detail"],
            "Please enter a valid question."
        )

    # Test missing question field
    def test_missing_question(self):

        response = self.client.post(
            "/ask",
            json={}
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
