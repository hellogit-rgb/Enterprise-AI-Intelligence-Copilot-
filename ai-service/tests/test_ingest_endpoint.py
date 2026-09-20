import unittest

from app.ingestion import ingest_documents


class TestIngestDocuments(unittest.TestCase):
    def test_ingest_documents_from_payload(self):
        payload = [
            {
                'id': 'doc-1',
                'name': 'Contract.pdf',
                'section': 'Payment Terms',
                'pages': [
                    (2, 'Payment is due within thirty days from invoice date. Late fees activate after the due date.')
                ]
            }
        ]

        chunks = ingest_documents(payload)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]['document_id'], 'doc-1')
        self.assertEqual(chunks[0]['page'], 2)
        self.assertIn('thirty days', chunks[0]['content'].lower())


if __name__ == '__main__':
    unittest.main()
