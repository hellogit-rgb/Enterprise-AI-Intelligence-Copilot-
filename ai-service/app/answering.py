from __future__ import annotations

import re
from typing import Any, Dict, List


class GroundedAnswerGenerator:
    def __init__(self, minimum_score: float = 0.35):
        self.minimum_score = minimum_score

    @staticmethod
    def _score(hit: Dict[str, Any]) -> float:
        try:
            value = float(hit.get('score', 0.0))
        except (TypeError, ValueError):
            return 0.0
        return value / 100 if value > 1 else value

    @staticmethod
    def _sentences(text: str) -> List[str]:
        return [sentence.strip() for sentence in re.split(r'(?<=[.!?])\s+', text or '') if sentence.strip()]

    def generate(self, query: str, hits: List[Dict[str, Any]]) -> Dict[str, Any]:
        ranked_hits = sorted(hits or [], key=self._score, reverse=True)
        usable_hits = [hit for hit in ranked_hits if self._score(hit) >= self.minimum_score]
        if not usable_hits:
            return {
                'answer': 'I could not find enough evidence to answer this confidently.',
                'sources': [],
                'citations_verified': False,
                'needs_review': True,
                'evidence_count': 0,
            }

        selected = usable_hits[:3]
        evidence_sentences = []
        for hit in selected:
            evidence_sentences.extend(self._sentences(hit.get('content', ''))[:2])

        answer = ' '.join(evidence_sentences[:4])
        sources = [
            {
                'title': hit.get('document_name', 'Unknown document'),
                'page': hit.get('page', 1),
                'section': hit.get('section', 'General'),
                'chunk_id': hit.get('chunk_id', hit.get('id')),
            }
            for hit in selected
        ]

        return {
            'answer': answer,
            'sources': sources,
            'citations_verified': bool(answer and sources),
            'needs_review': len(selected) == 0,
            'evidence_count': len(selected),
        }
