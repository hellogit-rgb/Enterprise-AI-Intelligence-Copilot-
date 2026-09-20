import unittest

from app.tools import SQLQueryTool
from app.access_control import can_access_document


class TestSQLGovernance(unittest.TestCase):
    def test_blocks_multiple_statements(self):
        tool = SQLQueryTool()
        self.assertFalse(tool.validate('SELECT * FROM customers; SELECT * FROM orders'))

    def test_blocks_unknown_columns(self):
        tool = SQLQueryTool(allowed_columns={'customers': {'customer_name', 'region'}})
        self.assertFalse(tool.validate('SELECT secret_value FROM customers'))

    def test_limits_rows(self):
        tool = SQLQueryTool(max_rows=1)
        result = tool.execute('SELECT customer_name FROM customers LIMIT 10')
        self.assertLessEqual(len(result['rows']), 1)


class TestDocumentAccess(unittest.TestCase):
    def test_allows_matching_role(self):
        document = {'id': 'doc-1', 'allowed_roles': ['finance']}
        self.assertTrue(can_access_document(document, 'finance'))

    def test_denies_non_matching_role(self):
        document = {'id': 'doc-1', 'allowed_roles': ['finance']}
        self.assertFalse(can_access_document(document, 'sales'))

    def test_defaults_to_authenticated_users(self):
        self.assertTrue(can_access_document({'id': 'doc-1'}, 'sales'))


if __name__ == '__main__':
    unittest.main()
