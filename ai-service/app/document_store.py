from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class DocumentStore:
    def __init__(self, path: Optional[Union[Path, str]] = None):
        default_path = Path(__file__).resolve().parents[1] / 'data' / 'documents.json'
        self.path = Path(path or os.getenv('DOCUMENT_STORE_PATH', default_path))

    def list_documents(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        with self.path.open('r', encoding='utf-8') as handle:
            documents = json.load(handle)
        return documents if isinstance(documents, list) else []

    def upsert(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        current = {document['id']: document for document in self.list_documents()}
        for document in documents:
            if document.get('id') and document.get('name'):
                current[document['id']] = document

        saved = list(current.values())
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=self.path.parent, delete=False) as handle:
                json.dump(saved, handle, ensure_ascii=False, indent=2)
                handle.write('\n')
                temporary_path = Path(handle.name)
            temporary_path.replace(self.path)
        finally:
            if temporary_path and temporary_path.exists():
                temporary_path.unlink()
        return saved

    def delete(self, document_id: str) -> bool:
        documents = self.list_documents()
        remaining = [document for document in documents if document.get('id') != document_id]
        if len(remaining) == len(documents):
            return False
        self._write(remaining)
        return True

    def _write(self, documents: List[Dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open('w', encoding='utf-8') as handle:
            json.dump(documents, handle, ensure_ascii=False, indent=2)
            handle.write('\n')
