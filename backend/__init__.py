"""
Aethersite - Package initialization
"""
__version__ = "1.0.0"
__author__ = "Aethersite Team"

from .src.docmemory_core import AethersiteCore, DocumentMemory
from .src.auto_save_load import AethersiteAutoSystem
from .src.document_processor import DocumentProcessor, DocumentIngestionPipeline
from .src.search_engine import AethersiteSearchSystem, SemanticSearchEngine

def create_system(storage_path: str = "./docmemory_storage/"):
    """Create a new Aethersite system instance"""
    from .src.auto_save_load import AethersiteAutoSystem
    return AethersiteAutoSystem(storage_path)