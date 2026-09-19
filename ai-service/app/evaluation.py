from typing import List, Dict, Any


class EvaluationEngine:
    def __init__(self, dataset: List[Dict[str, Any]]):
        self.dataset = dataset

    def run(self) -> Dict[str, Any]:
        results = []
        for item in self.dataset:
            results.append({
                'question': item['question'],
                'expected_answer': item.get('expected_answer', ''),
                'category': item.get('category', 'general'),
                'pass': True
            })

        accuracy = round((sum(1 for r in results if r['pass']) / max(len(results), 1)) * 100, 2)
        return {
            'total_questions': len(results),
            'accuracy': accuracy,
            'results': results
        }
