import unittest

from app.answering import GroundedAnswerGenerator


class TestGroundedAnswerGenerator(unittest.TestCase):
    def test_answers_from_retrieved_evidence(self):
        generator = GroundedAnswerGenerator()
        result = generator.generate(
            'What are the payment terms?',
            [
                {
                    'document_name': 'Contract.pdf',
                    'page': 4,
                    'section': 'Payment Terms',
                    'content': 'Payment shall be completed within thirty days from the invoice date.',
                    'score': 0.91,
                }
            ],
        )

        self.assertIn('thirty days', result['answer'].lower())
        self.assertEqual(result['sources'][0]['title'], 'Contract.pdf')
        self.assertTrue(result['citations_verified'])
        self.assertFalse(result['needs_review'])

    def test_marks_missing_evidence_for_review(self):
        result = GroundedAnswerGenerator().generate('What are the payment terms?', [])

        self.assertTrue(result['needs_review'])
        self.assertFalse(result['citations_verified'])
        self.assertEqual(result['answer'], 'I could not find enough evidence to answer this confidently.')


if __name__ == '__main__':
    unittest.main()
