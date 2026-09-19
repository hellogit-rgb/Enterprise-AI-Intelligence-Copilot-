from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class DocumentChunk:
    document_id: str
    document_name: str
    page: int
    section: str
    chunk_id: str
    text: str

    @property
    def content(self) -> str:
        return self.text

    def to_retrieval_dict(self) -> Dict[str, Any]:
        return {
            'id': self.chunk_id,
            'document_name': self.document_name,
            'page': self.page,
            'section': self.section,
            'content': self.text,
            'document_id': self.document_id,
            'chunk_id': self.chunk_id,
        }


class DocumentIngestionPipeline:
    def __init__(self, documents: List[Dict[str, Any]]):
        self.documents = documents

    @staticmethod
    def chunk_text(text: str, max_chars: int = 500, overlap: int = 80) -> List[str]:
        cleaned = ' '.join(text.split())
        if len(cleaned) <= max_chars:
            return [cleaned]

        chunks: List[str] = []
        start = 0
        while start < len(cleaned):
            end = min(start + max_chars, len(cleaned))
            segment = cleaned[start:end].strip()
            if not segment:
                break
            if end < len(cleaned):
                last_space = segment.rfind(' ')
                if last_space > int(max_chars * 0.65):
                    end = start + last_space
                    segment = cleaned[start:end].strip()
            chunks.append(segment)
            if end >= len(cleaned):
                break
            start = max(start + max_chars - overlap, end - overlap)
        return chunks

    def build_chunks(self) -> List[DocumentChunk]:
        chunks: List[DocumentChunk] = []
        for document in self.documents:
            for page_number, page_text in document.get('pages', []):
                section = document.get('section', 'General')
                page_chunks = self.chunk_text(page_text)
                for index, chunk_text in enumerate(page_chunks):
                    chunk = DocumentChunk(
                        document_id=document['id'],
                        document_name=document['name'],
                        page=page_number,
                        section=section,
                        chunk_id=f"{document['id']}_chunk_{index + 1}",
                        text=chunk_text,
                    )
                    chunks.append(chunk)
        return chunks


def build_sample_documents() -> List[Dict[str, Any]]:
    return [
        {
            'id': 'doc_1',
            'name': 'Customer_A_Contract.pdf',
            'section': 'Payment Terms',
            'pages': [
                (14, 'Payment shall be completed within thirty days from invoice date. Late payments incur a 2% penalty after the due date. The customer may request an extension only with written approval from finance.')
            ],
        },
        {
            'id': 'doc_2',
            'name': 'Payment_Policy.pdf',
            'section': 'Standard Terms',
            'pages': [
                (7, 'The standard payment policy states net 30 terms and instructs finance teams to review late fees as necessary. This policy applies to all regional customers unless a contract override is approved.')
            ],
        },
        {
            'id': 'doc_3',
            'name': 'Financial_Report.pdf',
            'section': 'Revenue Overview',
            'pages': [
                (31, 'Customer A generated 42.8 lakh in Q2, up from 36.4 lakh in Q1, representing an increase in quarterly revenue. Management highlighted stronger order volume and expanded product adoption.')
            ],
        },
    ]
