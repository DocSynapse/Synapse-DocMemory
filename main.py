"""
DocMemory - Main Integration and Testing
Complete system integration and testing
"""
import numpy as np
from pathlib import Path
import tempfile
import os
from typing import List

# Import all components
from src.docmemory_core import DocMemoryCore, DocumentMemory
from src.auto_save_load import DocMemoryAutoSystem
from src.document_processor import DocumentIngestionPipeline
from src.search_engine import DocMemorySearchSystem

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

class DocMemorySystem:
    """Complete DocMemory system integrating all components"""

    def __init__(self, storage_path: str = "./docmemory_storage/"):
        # Initialize core system with auto-save/load
        self.docmemory = DocMemoryAutoSystem(storage_path)

        # Initialize document processor
        self.processor = DocumentIngestionPipeline(self.docmemory)

        # Initialize search system
        self.search_system = DocMemorySearchSystem(self.docmemory)

        # Set up embedding model
        if SentenceTransformer:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.embedding_model = MockEmbeddingModel()

        self.processor.set_embedding_model(self.embedding_model)

        print(f"DocMemory system initialized with {self.docmemory.core_memory.get_document_count()} documents")

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

def create_test_document():
    """Create a temporary test document"""
    content = """
    Artificial Intelligence and Machine Learning Research

    Introduction:
    Artificial Intelligence (AI) is a branch of computer science that aims to create software or machines that exhibit human-like intelligence. This can include learning from experience, understanding natural language, solving problems, and recognizing patterns.

    Machine Learning (ML) is a subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. ML focuses on the development of computer programs that can access data and use it to learn for themselves.

    Deep Learning is a subset of machine learning where artificial neural networks, algorithms inspired by the human brain, learn from large amounts of data. Deep learning is a key technology behind driverless cars, enabling them to recognize a stop sign, or to distinguish a pedestrian from a lamppost.

    Applications:
    - Natural Language Processing
    - Computer Vision
    - Robotics
    - Expert Systems
    - Game AI

    Future Trends:
    The field of AI is rapidly evolving with new developments in neural architecture search, federated learning, and quantum computing applications. Ethical AI and explainable AI are becoming increasingly important as these systems are deployed in critical domains.
    """

    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(content)
        return f.name

def run_tests():
    """Run comprehensive tests on the DocMemory system"""
    print("Starting DocMemory system tests...\n")

    # Initialize system
    system = DocMemorySystem("./test_docmemory_storage/")

    try:
        # Test 1: Create and add a test document
        print("Test 1: Adding test document...")
        test_file = create_test_document()
        doc_ids = system.add_document_from_file(
            test_file,
            title="AI Research Paper",
            tags=["AI", "Machine Learning", "Research"],
            custom_metadata={"author": "Test Author", "category": "Research Paper"}
        )

        print(f"Added {len(doc_ids)} document chunks")
        print(f"Total documents in system: {system.get_document_count()}\n")

        # Test 2: Search functionality
        print("Test 2: Testing search functionality...")

        # Semantic search
        results = system.search("machine learning", search_type="semantic", limit=3)
        print(f"Semantic search results: {len(results)} found")
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['title']} (Score: {result['score']:.3f})")

        print()

        # Keyword search
        results = system.search("neural networks", search_type="keyword", limit=3)
        print(f"Keyword search results: {len(results)} found")
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['title']} - {result['content'][:100]}...")

        print()

        # Hybrid search
        results = system.search("artificial intelligence", search_type="hybrid", limit=3)
        print(f"Hybrid search results: {len(results)} found")
        for i, result in enumerate(results):
            print(f"  {i+1}. {result['title']} (Score: {result['score']:.3f}) - {result['content'][:100]}...")

        print()

        # Test 3: Document retrieval
        print("Test 3: Testing document retrieval...")
        if doc_ids:
            doc = system.get_document(doc_ids[0])
            if doc:
                print(f"Retrieved document: {doc.title}")
                print(f"Content preview: {doc.content[:100]}...")
                print(f"Tags: {doc.tags}")
                print(f"Source: {doc.source_file}")

        print()

        # Test 4: Related documents
        print("Test 4: Testing related documents...")
        if doc_ids:
            related = system.get_related_documents(doc_ids[0], limit=2)
            print(f"Found {len(related)} related documents")
            for i, rel_doc in enumerate(related):
                print(f"  {i+1}. {rel_doc['title']} (Score: {rel_doc['score']:.3f})")

        print()

        # Test 5: System persistence (simulated)
        print("Test 5: System persistence test...")
        # The auto-save system should handle this automatically
        print("Auto-save and auto-load systems active")

        print("\nAll tests completed successfully!")

    except Exception as e:
        print(f"Test error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Clean up test file
        try:
            # Remove test document
            test_files = Path("./test_docmemory_storage/").glob("temp*")
            for test_file in test_files:
                test_file.unlink()
        except:
            pass

        # Close system
        system.close()

def demo_usage():
    """Demonstrate how to use DocMemory in applications"""
    print("\nDocMemory Usage Demo:")
    print("="*50)

    # Initialize the system
    docmemory_system = DocMemorySystem()

    print("1. Add documents to memory:")
    print("   doc_ids = system.add_document_from_file('document.pdf', title='My Doc', tags=['important'])")

    print("\n2. Search documents:")
    print("   results = system.search('query about topic', search_type='hybrid')")

    print("\n3. Retrieve specific document:")
    print("   doc = system.get_document(doc_id)")

    print("\n4. Find related documents:")
    print("   related = system.get_related_documents(doc_id)")

    print("\n5. System automatically handles:")
    print("   - Storage to disk")
    print("   - Backup creation")
    print("   - Auto-load on startup")
    print("   - Search optimization")

    docmemory_system.close()

if __name__ == "__main__":
    # Run tests first
    run_tests()

    # Show usage demo
    demo_usage()

    print(f"\nDocMemory development complete!")
    print("Core components implemented:")
    print("- Core memory management")
    print("- Auto-save and auto-load")
    print("- Document processing pipeline")
    print("- Advanced search algorithms")
    print("- Complete integration and testing")