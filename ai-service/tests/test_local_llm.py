import unittest

from app.answering import GroundedAnswerGenerator


class TestLocalAnswerProvider(unittest.TestCase):
    def test_deterministic_fallback_is_available_without_paid_provider(self):
        result = GroundedAnswerGenerator().generate(
            'What are the payment terms?',
            [{'document_name': 'Policy.txt', 'page': 1, 'section': 'Terms', 'content': 'Net 30 applies.', 'score': 0.9}],
        )

        self.assertEqual(result['provider'], 'deterministic-local')
        self.assertIn('Net 30', result['answer'])


if __name__ == '__main__':
    unittest.main()
