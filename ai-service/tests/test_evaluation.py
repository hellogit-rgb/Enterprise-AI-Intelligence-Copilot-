import unittest

from app.evaluation import EvaluationEngine, load_sample_dataset


class TestEvaluationEngine(unittest.TestCase):
    def test_loads_default_dataset(self):
        dataset = load_sample_dataset()
        self.assertGreater(len(dataset), 0)
        self.assertIn('question', dataset[0])

    def test_run_returns_accuracy_summary(self):
        dataset = [
            {'question': 'What is the payment term?', 'expected_answer': '30 days', 'category': 'document'},
            {'question': 'Who has the highest revenue?', 'expected_answer': 'Top 5 by revenue', 'category': 'sql'},
        ]
        result = EvaluationEngine(dataset).run()
        self.assertEqual(result['total_questions'], 2)
        self.assertEqual(result['accuracy'], 100.0)
        self.assertEqual(len(result['results']), 2)


if __name__ == '__main__':
    unittest.main()
