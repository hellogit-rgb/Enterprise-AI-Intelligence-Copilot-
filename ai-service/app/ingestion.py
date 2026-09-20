from __future__ import annotations

import base64
import binascii
import io
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional


@dataclass
class DocumentChunk:
    document_id: str
    document_name: str
    page: int
    section: str
    chunk_id: str
    text: str
    allowed_roles: Optional[List[str]] = None

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
            'allowed_roles': self.allowed_roles or [],
        }


class DocumentIngestionPipeline:
    def __init__(self, documents: List[Dict[str, Any]]):
        self.documents = documents

    @staticmethod
    def chunk_text(text: str, max_chars: int = 500, overlap: int = 80) -> List[str]:
        cleaned = ' '.join((text or '').split())
        if not cleaned:
            return []
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
            pages = document.get('pages')
            if pages:
                for page_number, page_text in pages:
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
                            allowed_roles=document.get('allowed_roles'),
                        )
                        chunks.append(chunk)
                continue

            raw_text = document.get('text', '')
            section = document.get('section', 'General')
            page_chunks = self.chunk_text(raw_text)
            for index, chunk_text in enumerate(page_chunks):
                chunk = DocumentChunk(
                    document_id=document['id'],
                    document_name=document['name'],
                    page=1,
                    section=section,
                    chunk_id=f"{document['id']}_chunk_{index + 1}",
                    text=chunk_text,
                    allowed_roles=document.get('allowed_roles'),
                )
                chunks.append(chunk)
        return chunks


def ingest_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pipeline = DocumentIngestionPipeline(documents)
    return [chunk.to_retrieval_dict() for chunk in pipeline.build_chunks()]


def document_from_file(name: str, content_base64: str, section: str = 'General') -> Dict[str, Any]:
    extension = Path(name).suffix.lower()
    if extension not in {'.txt', '.md', '.csv', '.json', '.pdf'}:
        raise ValueError('Only text, markdown, CSV, JSON, and PDF files are supported.')

    try:
        file_bytes = base64.b64decode(content_base64, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise ValueError('File content must be valid base64.') from exc

    document = {'name': name, 'section': section}
    if extension == '.pdf':
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            document['pages'] = [
                (page_number, page.extract_text() or '')
                for page_number, page in enumerate(reader.pages, start=1)
            ]
        except Exception as exc:
            raise ValueError('The PDF could not be read.') from exc
    else:
        try:
            document['text'] = file_bytes.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError('Text files must use UTF-8 encoding.') from exc

    return document


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
