import unittest
from unittest.mock import patch

import pandas as pd

from src.finance_chat import (
    build_financial_summary,
    detect_intent,
)
from src.ml_expense_prediction import (
    prepare_dataset,
    train_model,
)
from src.anomaly_detection import detect_anomalies
from src.llm_client import _mock_response


class TestFinanceChat(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame(
            {
                "type": [
                    "Income",
                    "Expense",
                    "Expense",
                    "Expense",
                ],
                "category": [
                    "Salary",
                    "Food",
                    "Shopping",
                    "Transport",
                ],
                "amount": [
                    50000,
                    5000,
                    8000,
                    2000,
                ],
            }
        )

    def test_financial_summary(self):
        summary = build_financial_summary(self.df)

        self.assertEqual(summary["income"], 50000.0)
        self.assertEqual(summary["expenses"], 15000.0)
        self.assertEqual(summary["savings"], 35000.0)
        self.assertAlmostEqual(summary["savings_rate"], 70.0)
        self.assertEqual(summary["highest_category"], "Shopping")
        self.assertEqual(
            summary["highest_category_amount"],
            8000.0,
        )

    def test_intent_detection(self):
        cases = {
            "How much did I earn?": "income",
            "How much did I spend?": "expenses",
            "What are my savings?": "savings",
            "How much did I spend on Shopping?": "category",
            "What is my predicted expense?": "prediction",
            "Did you detect unusual spending?": "anomaly",
            "Compare my predicted spending with current spending": "comparison",
            "Give me a financial overview": "general",
        }

        for question, expected in cases.items():
            with self.subTest(question=question):
                self.assertEqual(
                    detect_intent(question),
                    expected,
                )


class TestExpensePrediction(unittest.TestCase):

    def test_prepare_dataset(self):
        dates = pd.date_range(
            "2026-01-01",
            periods=15,
            freq="D",
        )

        df = pd.DataFrame(
            {
                "date": dates,
                "amount": [
                    100 + i * 10
                    for i in range(15)
                ],
            }
        )

        prepared = prepare_dataset(df)

        self.assertFalse(prepared.empty)
        self.assertIn(
            "day_of_week",
            prepared.columns,
        )
        self.assertIn(
            "previous_day_expense",
            prepared.columns,
        )
        self.assertIn(
            "previous_7_day_expense",
            prepared.columns,
        )
        self.assertIn(
            "rolling_7_day_avg",
            prepared.columns,
        )
        self.assertFalse(
            prepared.isna().any().any()
        )

    def test_train_model(self):
        dates = pd.date_range(
            "2026-01-01",
            periods=40,
            freq="D",
        )

        df = pd.DataFrame(
            {
                "date": dates,
                "amount": [
                    100
                    + (i % 7) * 20
                    + i * 2
                    for i in range(40)
                ],
            }
        )

        prepared = prepare_dataset(df)

        model, mae, rmse, r2 = train_model(
            prepared
        )

        self.assertIsNotNone(model)
        self.assertGreaterEqual(mae, 0)
        self.assertGreaterEqual(rmse, 0)
        self.assertIsInstance(r2, float)


class TestAnomalyDetection(unittest.TestCase):

    @patch(
        "src.anomaly_detection.get_expense_data"
    )
    def test_anomaly_detection_output(
        self,
        mock_get_expense_data,
    ):
        dates = pd.date_range(
            "2026-01-01",
            periods=20,
            freq="D",
        )

        amounts = [
            100, 105, 98, 110, 102,
            97, 108, 101, 99, 104,
            103, 106, 100, 98, 107,
            102, 101, 109, 103, 5000,
        ]

        mock_get_expense_data.return_value = pd.DataFrame(
            {
                "id": range(1, 21),
                "date": dates,
                "category": ["Food"] * 20,
                "description": ["Test expense"] * 20,
                "amount": amounts,
                "payment_method": ["Cash"] * 20,
            }
        )

        result = detect_anomalies()

        self.assertIsNotNone(result)

        self.assertIn(
            "anomaly_prediction",
            result.columns,
        )

        self.assertIn(
            "anomaly_score",
            result.columns,
        )

        self.assertIn(
            "status",
            result.columns,
        )

        anomalies = result[
            result["anomaly_prediction"] == -1
        ]

        self.assertGreaterEqual(
            len(anomalies),
            1,
        )


class TestMockLLM(unittest.TestCase):

    def test_mock_llm_uses_financial_context(self):
        prompt = """
Total income: ₹50,000.00
Total expenses: ₹15,000.00
Savings: ₹35,000.00
Savings rate: 70.00%
Highest spending category: Shopping
Highest category spending: ₹8,000.00
"""

        response = _mock_response(prompt)

        self.assertIn(
            "₹50,000.00",
            response,
        )

        self.assertIn(
            "₹15,000.00",
            response,
        )

        self.assertIn(
            "₹35,000.00",
            response,
        )

        self.assertIn(
            "Shopping",
            response,
        )


if __name__ == "__main__":
    unittest.main()