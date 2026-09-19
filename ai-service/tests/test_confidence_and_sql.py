import unittest

from app.confidence import ConfidenceEngine
from app.tools import SQLQueryTool


class TestSQLSecurity(unittest.TestCase):
    def test_allows_safe_select_statement(self):
        tool = SQLQueryTool(allowed_tables={"customers", "orders"})
        query = "SELECT customer_name FROM customers WHERE region = 'NA' LIMIT 10"
        self.assertTrue(tool.validate(query))

    def test_blocks_destructive_sql(self):
        tool = SQLQueryTool()
        self.assertFalse(tool.validate("DROP TABLE customers"))

    def test_blocks_unauthorized_table(self):
        tool = SQLQueryTool(allowed_tables={"customers"})
        self.assertFalse(tool.validate("SELECT * FROM sales"))


class TestConfidenceEngine(unittest.TestCase):
    def test_requires_review_for_low_confidence(self):
        engine = ConfidenceEngine()
        result = engine.score(
            "What are the customer payment terms?",
            [{"score": 0.05, "document_name": "weak.pdf"}],
            "DocumentSearchTool",
        )
        self.assertFalse(result["is_confident"])
        self.assertTrue(result["needs_review"])

    def test_rewards_relevant_evidence(self):
        engine = ConfidenceEngine()
        result = engine.score(
            "What are the customer payment terms?",
            [
                {"score": 0.82, "document_name": "Customer_A_Contract.pdf"},
                {"score": 0.76, "document_name": "Payment_Policy.pdf"},
            ],
            "DocumentSearchTool",
        )
        self.assertGreater(result["score"], 0.7)
        self.assertTrue(result["is_confident"])


if __name__ == "__main__":
    unittest.main()
