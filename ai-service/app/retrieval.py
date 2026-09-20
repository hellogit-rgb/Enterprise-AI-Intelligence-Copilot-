import re
from typing import List, Dict, Any

from rank_bm25 import BM25Okapi
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class HybridRetriever:
    def __init__(self, documents: List[Dict[str, Any]], model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.documents = documents
        self.model = SentenceTransformer(model_name) if SentenceTransformer else None
        self.corpus = [doc['content'] for doc in self.documents]
        self.bm25 = BM25Okapi([self._tokenize(doc['content']) for doc in self.documents])
        self.embeddings = (
            self.model.encode(self.corpus, convert_to_numpy=True, show_progress_bar=False)
            if self.model else None
        )

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def search(self, query: str, top_k: int = 5, alpha: float = 0.7, beta: float = 0.3) -> List[Dict[str, Any]]:
        query_tokens = self._tokenize(query)
        bm25_scores = self.bm25.get_scores(query_tokens)
        if self.model:
            query_embedding = self.model.encode([query], convert_to_numpy=True, show_progress_bar=False)[0]
            semantic_scores = self._cosine_similarity(query_embedding, self.embeddings)
        else:
            semantic_scores = self._lexical_similarity(query_tokens)

        combined = []
        for idx, doc in enumerate(self.documents):
            hybrid_score = (alpha * semantic_scores[idx]) + (beta * bm25_scores[idx])
            combined.append({
                'id': doc.get('id', idx),
                'document_name': doc.get('document_name', 'unknown.pdf'),
                'page': doc.get('page', 1),
                'section': doc.get('section', 'General'),
                'content': doc['content'],
                'allowed_roles': doc.get('allowed_roles', []),
                'score': float(hybrid_score)
            })

        return sorted(combined, key=lambda item: item['score'], reverse=True)[:top_k]

    @staticmethod
    def _cosine_similarity(query_embedding, embeddings):
        import numpy as np
        norms = np.linalg.norm(embeddings, axis=1)
        query_norm = np.linalg.norm(query_embedding)
        if query_norm == 0:
            return np.zeros(len(embeddings))
        return np.dot(embeddings, query_embedding) / (norms * query_norm)

    def _lexical_similarity(self, query_tokens: List[str]):
        query_set = set(query_tokens)
        if not query_set:
            return [0.0] * len(self.documents)
        scores = []
        for document in self.documents:
            document_set = set(self._tokenize(document['content']))
            union = query_set | document_set
            scores.append(len(query_set & document_set) / len(union) if union else 0.0)
        return scores
