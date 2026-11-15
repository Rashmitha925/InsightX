
import unittest
import pandas as pd

from src.tools.dataset_tool import analyze_dataset


class TestDatasetTool(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Employee": ["A", "B", "C"],
            "Salary": [30000, 40000, 50000],
            "Age": [22, 25, None]
        })

    def test_row_count(self):
        result = analyze_dataset(
            "How many rows are there?",
            self.df
        )
        self.assertEqual(result["result"], 3)
        self.assertEqual(result["operation"], "row_count")

    def test_column_count(self):
        result = analyze_dataset(
            "How many columns are there?",
            self.df
        )
        self.assertEqual(result["result"], 3)
        self.assertEqual(result["operation"], "column_count")

    def test_column_names(self):
        result = analyze_dataset(
            "Show column names",
            self.df
        )
        self.assertEqual(
            result["result"],
            ["Employee", "Salary", "Age"]
        )

    def test_missing_values(self):
        result = analyze_dataset(
            "How many missing values?",
            self.df
        )
        self.assertEqual(result["result"], 1)

    def test_average(self):
        result = analyze_dataset(
            "What is the average Salary?",
            self.df
        )
        self.assertEqual(result["result"], 40000.0)

    def test_maximum(self):
        result = analyze_dataset(
            "What is the maximum Salary?",
            self.df
        )
        self.assertEqual(result["result"], 50000.0)

    def test_unsupported_question(self):
        result = analyze_dataset(
            "Predict next year's employee performance",
            self.df
        )
        self.assertEqual(result["operation"], "unsupported")

    def test_empty_question(self):
        with self.assertRaises(ValueError):
            analyze_dataset("", self.df)

    def test_empty_dataset(self):
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            analyze_dataset("How many rows?", empty_df)

    def test_average_without_valid_column(self):
        with self.assertRaises(ValueError):
            analyze_dataset(
                "What is the average department?",
                self.df
            )


if __name__ == "__main__":
    unittest.main()
