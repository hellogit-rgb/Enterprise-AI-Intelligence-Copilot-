import re
from typing import Any, Dict, Iterable, List


class ConfidenceEngine:
    """Estimate confidence for document-search and SQL responses."""

    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold

    @staticmethod
    def _normalize_score(value: Any) -> float:
        try:
            score = float(value)
        except (TypeError, ValueError):
            return 0.0

        if score > 1:
            score = score / 100.0
        return max(0.0, min(1.0, score))

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return {
            token.lower()
            for token in re.findall(r"[a-zA-Z0-9]+", text or "")
            if token.lower() not in {"the", "what", "are", "for", "with", "from", "and", "about", "which"}
        }

    def score(self, query: str, hits: Iterable[Dict[str, Any]], tool_name: str) -> Dict[str, Any]:
        hits = list(hits or [])
        if not hits:
            base = 0.3 if tool_name == "DocumentSearchTool" else 0.45
            return {
                "score": round(base, 3),
                "is_confident": False,
                "needs_review": True,
                "tool": tool_name,
                "reason": "No evidence was returned for this query."
            }

        normalized_scores = [self._normalize_score(hit.get("score", 0.0)) for hit in hits]
        relevance_mean = sum(normalized_scores) / len(normalized_scores)

        query_terms = self._tokenize(query)
        overlap = 0.0
        if query_terms:
            document_terms = set()
            for hit in hits:
                document_terms |= self._tokenize(hit.get("document_name", ""))
                document_terms |= self._tokenize(hit.get("content", ""))
            overlap = len(query_terms & document_terms) / len(query_terms)

        confidence_score = min(1.0, relevance_mean * 0.75 + overlap * 0.25)
        if tool_name == "SQLQueryTool":
            confidence_score = min(1.0, confidence_score + 0.1)

        confidence_score = max(0.0, min(1.0, confidence_score))
        is_confident = confidence_score >= self.threshold

        return {
            "score": round(confidence_score, 3),
            "is_confident": is_confident,
            "needs_review": not is_confident,
            "tool": tool_name,
            "reason": "The evidence quality is sufficient for a confident answer." if is_confident else "The evidence is weak or sparse; human review is recommended."
        }
