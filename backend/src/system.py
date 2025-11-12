# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

"""
Aethersite System
The main Aethersite system class
"""
import numpy as np
from typing import List
from .docmemory_core import DocumentMemory
from .auto_save_load import AethersiteAutoSystem
from .document_processor import DocumentIngestionPipeline
from .search_engine import AethersiteSearchSystem

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None
    print("Warning: sentence-transformers not available. Using mock embeddings.")

class MockEmbeddingModel:
    """Mock embedding model for testing when sentence-transformers is not available"""
    def __init__(self):
        self.embedding_dim = 384

    def encode(self, sentences):
        """Generate mock embeddings for testing"""
        embeddings = []
        for sentence in sentences:
            # Create deterministic embeddings based on sentence content
            hash_val = hash(sentence) % (2**32)
            embedding = np.frombuffer(hash_val.to_bytes(4, 'big') * 96, dtype=np.float32)[:self.embedding_dim]
            embedding = embedding / np.linalg.norm(embedding)  # Normalize
            embeddings.append(embedding)
        return np.array(embeddings)

class AethersiteSystem:
    """Complete Aethersite system integrating all components"""

    def __init__(self, storage_path: str = "./docmemory_storage/"):
        # Initialize core system with auto-save/load
        self.docmemory = AethersiteAutoSystem(storage_path)

        # Initialize document processor
        self.processor = DocumentIngestionPipeline(self.docmemory)

        # Initialize search system
        self.search_system = AethersiteSearchSystem(self.docmemory)

        # Set up embedding model
        if SentenceTransformer:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.embedding_model = MockEmbeddingModel()

        self.processor.set_embedding_model(self.embedding_model)

        print(f"Aethersite system initialized with {self.docmemory.core_memory.get_document_count()} documents")

    def add_document_from_file(self,
                              file_path: str,
                              title: str = None,
                              tags: List[str] = None,
                              custom_metadata: dict = None) -> List[str]:
        """Add a document file to the memory system"""
        try:
            doc_ids = self.processor.process_and_store_document(
                file_path=file_path,
                title=title,
                tags=tags,
                custom_metadata=custom_metadata
            )
            print(f"Added {len(doc_ids)} document chunks from {file_path}")
            return doc_ids
        except Exception as e:
            print(f"Error adding document {file_path}: {e}")
            return []

    def search(self,
               query: str,
               search_type: str = "hybrid",
               limit: int = 10) -> list:
        """Search documents"""
        # Generate embedding for the query
        query_embedding = self.embedding_model.encode([query])[0]

        results = self.search_system.search(
            query=query,
            query_embedding=query_embedding,
            search_type=search_type,
            limit=limit
        )
        return results

    def get_document(self, doc_id: str) -> DocumentMemory:
        """Get a specific document"""
        return self.docmemory.get_document(doc_id)

    def get_document_count(self) -> int:
        """Get the total number of documents"""
        return self.docmemory.core_memory.get_document_count()

    def get_related_documents(self, doc_id: str, limit: int = 5) -> list:
        """Get documents related to a specific document"""
        return self.search_system.find_related_documents(doc_id, limit)

    def close(self):
        """Close the system gracefully"""
        self.docmemory.close()
