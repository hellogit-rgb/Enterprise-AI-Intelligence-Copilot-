import unittest

from app.ingestion import DocumentIngestionPipeline


class TestDocumentIngestion(unittest.TestCase):
    def test_builds_metadata_aware_chunks(self):
        documents = [
            {
                'id': 'doc-123',
                'name': 'Customer_A_Contract.pdf',
                'section': 'Payment Terms',
                'pages': [
                    (1, 'Payment is due within thirty days from invoice date. Late fees apply after the due date. The customer may request extension only with written approval.')
                ]
            }
        ]

        chunks = DocumentIngestionPipeline(documents).build_chunks()

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].document_id, 'doc-123')
        self.assertEqual(chunks[0].page, 1)
        self.assertEqual(chunks[0].section, 'Payment Terms')
        self.assertIn('thirty days', chunks[0].text.lower())

    def test_supports_raw_text_documents(self):
        documents = [
            {
                'id': 'doc-456',
                'name': 'Policy.txt',
                'section': 'Standard Terms',
                'text': 'Net 30 applies to all customers. Late fees are reviewed at the end of each month.'
            }
        ]

        chunks = DocumentIngestionPipeline(documents).build_chunks()

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].document_name, 'Policy.txt')
        self.assertEqual(chunks[0].page, 1)


if __name__ == '__main__':
    unittest.main()
