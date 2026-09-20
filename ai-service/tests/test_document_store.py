import tempfile
import unittest
from pathlib import Path

from app.document_store import DocumentStore


class TestDocumentStore(unittest.TestCase):
    def test_saves_lists_and_replaces_documents(self):
        with tempfile.TemporaryDirectory() as directory:
            store = DocumentStore(Path(directory) / 'documents.json')
            first = [{'id': 'doc-1', 'name': 'Policy.txt', 'content': 'Net 30'}]
            replacement = [{'id': 'doc-1', 'name': 'Policy.txt', 'content': 'Net 45'}]

            store.upsert(first)
            store.upsert(replacement)

            documents = store.list_documents()
            self.assertEqual(len(documents), 1)
            self.assertEqual(documents[0]['content'], 'Net 45')

    def test_loads_documents_after_new_instance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'documents.json'
            DocumentStore(path).upsert([{'id': 'doc-2', 'name': 'Contract.txt', 'content': 'Payment terms'}])

            documents = DocumentStore(path).list_documents()

            self.assertEqual(documents[0]['id'], 'doc-2')


if __name__ == '__main__':
    unittest.main()
