# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

"""
Unit tests for document processor
"""
import pytest
import tempfile
from backend.src.document_processor import DocumentProcessor

def test_document_processing():
    """Test document processing functionality"""
    processor = DocumentProcessor()
    text = "This is a test document. It has multiple sentences."

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(text)
        file_path = f.name

    chunks = processor.process_document(file_path)

    assert len(chunks) > 0
    assert "This is a test document." in chunks[0].content
