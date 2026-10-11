"""
Unit tests for RAG tools, document loading, and chunking logic.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.rag_tools import load_documents, split_documents


class TestRAGTools(unittest.TestCase):
    def test_load_documents_finds_handbook(self):
        docs = load_documents()
        self.assertGreater(len(docs), 0, "Harus menemukan setidaknya dokumen company_handbook.md")
        filenames = [d.metadata.get("source_filename") for d in docs]
        self.assertIn("company_handbook.md", filenames)

    def test_split_documents_chunks(self):
        docs = load_documents()
        chunks = split_documents(docs)
        self.assertGreater(len(chunks), len(docs), "Hasil chunking harus memecah dokumen menjadi potongan-potongan teks")
        for chunk in chunks:
            self.assertIsNotNone(chunk.page_content)
            self.assertGreater(len(chunk.page_content), 10)


if __name__ == "__main__":
    unittest.main()
