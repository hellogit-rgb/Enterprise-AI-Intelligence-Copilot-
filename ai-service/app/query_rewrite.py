import re


class QueryRewriter:
    @staticmethod
    def rewrite(query: str, context: str = '') -> str:
        q = query.strip()
        lowered = q.lower()

        if not q:
            return ''

        if 'payment' in lowered and 'what about' in lowered:
            return 'What are the payment terms mentioned in the currently selected customer contract?'

        if 'what about' in lowered:
            return q.replace('what about', 'What is the relevant information for')

        if len(q.split()) <= 3 and 'customer' in lowered:
            return f"Provide the relevant customer details for: {q}"

        if 'payment' in lowered and 'contract' in lowered:
            return q

        return q
