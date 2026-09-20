import base64
import io
import unittest

from app.ingestion import document_from_file
from pypdf import PdfWriter


class TestFileIngestion(unittest.TestCase):
    def test_decodes_text_file(self):
        encoded = base64.b64encode(b'Net 30 payment terms apply.').decode('ascii')

        document = document_from_file('Policy.txt', encoded, 'Standard Terms')

        self.assertEqual(document['name'], 'Policy.txt')
        self.assertEqual(document['section'], 'Standard Terms')
        self.assertEqual(document['text'], 'Net 30 payment terms apply.')

    def test_rejects_unsupported_extension(self):
        encoded = base64.b64encode(b'content').decode('ascii')

        with self.assertRaises(ValueError):
            document_from_file('Policy.docx', encoded, 'General')

    def test_reads_pdf_pages(self):
        output = io.BytesIO()
        writer = PdfWriter()
        writer.add_blank_page(width=300, height=300)
        writer.write(output)
        encoded = base64.b64encode(output.getvalue()).decode('ascii')

        document = document_from_file('Report.pdf', encoded, 'Reports')

        self.assertEqual(document['name'], 'Report.pdf')
        self.assertEqual(len(document['pages']), 1)


if __name__ == '__main__':
    unittest.main()
