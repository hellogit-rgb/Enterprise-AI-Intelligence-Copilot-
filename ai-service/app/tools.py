import re
from typing import List, Dict, Any


class DocumentSearchTool:
    def __init__(self, retriever):
        self.retriever = retriever

    def execute(self, query: str, top_k: int = 5):
        return self.retriever.search(query, top_k=top_k)


class SQLQueryTool:
    def __init__(self, allowed_tables=None):
        self.allowed_tables = allowed_tables or {'customers', 'sales', 'transactions', 'orders'}

    def validate(self, query: str) -> bool:
        if not query or not isinstance(query, str):
            return False

        normalized = query.strip()
        if not normalized:
            return False

        prohibited = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE', 'CREATE', 'GRANT', 'REVOKE']
        upper_query = normalized.upper()
        for keyword in prohibited:
            if keyword in upper_query:
                return False

        allowed_tokens = ['SELECT', 'WITH', 'GROUP', 'ORDER', 'WHERE', 'JOIN', 'LIMIT']
        if not any(token in upper_query for token in allowed_tokens):
            return False

        table_matches = re.findall(r'FROM\s+([A-Za-z_][A-Za-z0-9_]*)|JOIN\s+([A-Za-z_][A-Za-z0-9_]*)', normalized, flags=re.IGNORECASE)
        discovered_tables = {table for match in table_matches for table in match if table}
        if not discovered_tables:
            return False

        for table in discovered_tables:
            if table.lower() not in {name.lower() for name in self.allowed_tables}:
                return False

        return True

    def execute(self, query: str):
        if not self.validate(query):
            raise ValueError('Unsafe SQL query blocked.')
        return {
            'sql': query,
            'rows': [
                {'customer_name': 'Customer A', 'total_revenue': 4280000},
                {'customer_name': 'Customer B', 'total_revenue': 3560000}
            ]
        }


class CalculatorTool:
    def execute(self, value_a: float, value_b: float, operation: str = 'subtract'):
        if operation == 'subtract':
            return value_a - value_b
        if operation == 'percent_change':
            if value_b == 0:
                return 0
            return ((value_a - value_b) / value_b) * 100
        return value_a + value_b
