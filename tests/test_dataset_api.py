
import unittest
from io import BytesIO
from unittest.mock import patch

import pandas as pd
from fastapi.testclient import TestClient

from src.api.server import app


class TestDatasetAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

        self.df = pd.DataFrame({
            "Employee": ["A", "B", "C"],
            "Salary": [30000, 40000, 50000],
            "Age": [22, 25, 28]
        })

    def create_csv_file(self):
        csv_data = self.df.to_csv(index=False).encode("utf-8")
        return {
            "file": (
                "employees.csv",
                csv_data,
                "text/csv"
            )
        }

    def create_excel_file(self):
        excel_buffer = BytesIO()

        self.df.to_excel(
            excel_buffer,
            index=False,
            engine="openpyxl"
        )

        return {
            "file": (
                "employees.xlsx",
                excel_buffer.getvalue(),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        }

    # Test successful CSV upload and row count
    def test_csv_upload_row_count(self):
        response = self.client.post(
            "/ask-dataset",
            data={"question": "How many rows are there?"},
            files=self.create_csv_file()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["operation"],
            "row_count"
        )
        self.assertEqual(
            response.json()["tool_result"],
            3
        )

    # Test successful Excel upload and column count
    def test_excel_upload_column_count(self):
        response = self.client.post(
            "/ask-dataset",
            data={"question": "How many columns are there?"},
            files=self.create_excel_file()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["operation"],
            "column_count"
        )
        self.assertEqual(
            response.json()["tool_result"],
            3
        )

    # Test average calculation on uploaded CSV
    def test_csv_average_calculation(self):
        response = self.client.post(
            "/ask-dataset",
            data={"question": "What is the average Salary?"},
            files=self.create_csv_file()
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["tool_result"],
            40000.0
        )

    # Test rejection of unsupported file extension
    def test_unsupported_file_extension(self):
        response = self.client.post(
            "/ask-dataset",
            data={"question": "How many rows?"},
            files={
                "file": (
                    "employees.txt",
                    b"sample data",
                    "text/plain"
                )
            }
        )

        self.assertEqual(response.status_code, 400)

    # Test rejection of empty question
    def test_empty_question(self):
        response = self.client.post(
            "/ask-dataset",
            data={"question": ""},
            files=self.create_csv_file()
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"],
            "Please enter a valid question."
        )

    # Test rejection of invalid Excel contents
    def test_invalid_file_contents(self):
        response = self.client.post(
            "/ask-dataset",
            data={"question": "How many rows?"},
            files={
                "file": (
                    "employees.xlsx",
                    b"this is not a valid Excel file",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            }
        )

        self.assertEqual(response.status_code, 400)

    # Test rejection of a dataset with headers but no data rows
    def test_empty_dataset(self):
        empty_csv = b"Employee,Salary,Age\n"

        response = self.client.post(
            "/ask-dataset",
            data={"question": "How many rows?"},
            files={
                "file": (
                    "empty.csv",
                    empty_csv,
                    "text/csv"
                )
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"],
            "The uploaded dataset contains no data."
        )


if __name__ == "__main__":
    unittest.main()
