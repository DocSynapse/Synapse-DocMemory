"""
DocMemory - Package initialization
"""
__version__ = "1.0.0"
__author__ = "DocMemory Team"

from .src.docmemory_core import DocMemoryCore, DocumentMemory
from .src.auto_save_load import DocMemoryAutoSystem
from .src.document_processor import DocumentProcessor, DocumentIngestionPipeline
from .src.search_engine import DocMemorySearchSystem, SemanticSearchEngine

def create_system(storage_path: str = "./docmemory_storage/"):
    """Create a new DocMemory system instance"""
    from .src.auto_save_load import DocMemoryAutoSystem
    return DocMemoryAutoSystem(storage_path)