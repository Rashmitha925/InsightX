
import unittest

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


if __name__ == "__main__":
    unittest.main()
