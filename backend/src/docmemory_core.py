"""
Aethersite - Advanced Document Memory System
Core Memory Management Implementation
"""
import os
import json
import pickle
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import numpy as np
import sqlite3
import faiss
from dataclasses import dataclass, field
import threading

@dataclass
class DocumentMemory:
    """Represents a single document memory with metadata"""
    id: str
    content: str
    title: str
    source_file: str
    embedding: np.ndarray
    timestamp: datetime
    document_type: str  # pdf, docx, txt, etc.
    tags: List[str] = field(default_factory=list)
    relationships: Dict[str, float] = field(default_factory=dict)  # related doc_ids
    metadata: Dict[str, Any] = field(default_factory=dict)  # additional document metadata
    summary: str = ""
    page_numbers: List[int] = field(default_factory=list)  # if from multi-page doc

class AethersiteCore:
    """Core memory management system for documents"""
    
    def __init__(self, storage_path: str = "./docmemory_storage/"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # Thread-local storage for database connections
        self.local = threading.local()

        # Initialize storage components
        self._init_database()
        self._init_vector_index()
        
        # Memory stores
        self.document_memories = {}  # In-memory cache for active documents
        self.unsaved_changes = {}    # Track changes for auto-save
        
    def _get_db_connection(self):
        """Get a database connection for the current thread."""
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.local.conn.row_factory = sqlite3.Row
        return self.local.conn

    def _init_database(self):
        """Initialize SQLite database for metadata storage"""
        self.db_path = self.storage_path / "document_memories.db"
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_memories (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT,
                source_file TEXT,
                timestamp TEXT,
                document_type TEXT,
                tags TEXT,
                relationships TEXT,
                metadata TEXT,
                summary TEXT,
                page_numbers TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_embeddings (
                id TEXT PRIMARY KEY,
                embedding BLOB,
                FOREIGN KEY (id) REFERENCES document_memories (id)
            )
        ''')
        
        conn.commit()
    
    def _init_vector_index(self):
        """Initialize FAISS vector index for similarity search"""
        self.embedding_dim = 384  # Using smaller dimension for efficiency
        self.faiss_index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product (cosine similarity)
        
        # Initialize mapping between FAISS index and document IDs
        self.id_to_index = {}  # document_id -> FAISS index
        self.index_to_id = {}  # FAISS index -> document_id
        
        # Load existing embeddings if they exist
        self._load_existing_embeddings()
    
    def _load_existing_embeddings(self):
        """Load existing embeddings from database to FAISS index"""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, embedding FROM document_embeddings ORDER BY id")
        
        index_counter = 0
        for row in cursor.fetchall():
            doc_id = row['id']
            embedding_bytes = row['embedding']
            
            # Convert bytes back to numpy array
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            embedding = embedding / np.linalg.norm(embedding)  # Normalize
            
            # Add to FAISS index
            self.faiss_index.add(embedding.reshape(1, -1))
            
            # Update mappings
            self.id_to_index[doc_id] = index_counter
            self.index_to_id[index_counter] = doc_id
            index_counter += 1
    
    def store_document(self, 
                     content: str, 
                     title: str, 
                     source_file: str,
                     embedding: np.ndarray,
                     document_type: str = "unknown",
                     tags: List[str] = None,
                     metadata: Dict[str, Any] = None,
                     summary: str = "",
                     page_numbers: List[int] = None) -> str:
        """Store a document in memory system"""
        
        doc_id = str(uuid.uuid4())
        
        # Normalize embedding
        embedding = embedding / np.linalg.norm(embedding)
        
        # Create document memory object
        doc_memory = DocumentMemory(
            id=doc_id,
            content=content,
            title=title,
            source_file=source_file,
            embedding=embedding,
            timestamp=datetime.now(),
            document_type=document_type,
            tags=tags or [],
            relationships={},
            metadata=metadata or {},
            summary=summary,
            page_numbers=page_numbers or []
        )
        
        # Store in database
        self._store_in_database(doc_memory)
        
        # Store embedding in vector database
        self._store_embedding(doc_id, embedding)
        
        # Add to in-memory cache
        self.document_memories[doc_id] = doc_memory
        self.unsaved_changes[doc_id] = doc_memory
        
        return doc_id
    
    def _store_in_database(self, doc_memory: DocumentMemory):
        """Store document metadata in SQLite database"""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO document_memories 
            (id, title, content, source_file, timestamp, document_type, tags, relationships, metadata, summary, page_numbers)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            doc_memory.id,
            doc_memory.title,
            doc_memory.content,
            doc_memory.source_file,
            doc_memory.timestamp.isoformat(),
            doc_memory.document_type,
            json.dumps(doc_memory.tags),
            json.dumps(doc_memory.relationships),
            json.dumps(doc_memory.metadata),
            doc_memory.summary,
            json.dumps(doc_memory.page_numbers)
        ))
        
        conn.commit()
    
    def _store_embedding(self, doc_id: str, embedding: np.ndarray):
        """Store document embedding in vector database"""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Convert numpy array to bytes
        embedding_bytes = embedding.astype(np.float32).tobytes()
        
        cursor.execute('''
            INSERT OR REPLACE INTO document_embeddings 
            (id, embedding) VALUES (?, ?)
        ''', (doc_id, embedding_bytes))
        
        conn.commit()
        
        # Update FAISS index
        embedding_normalized = embedding / np.linalg.norm(embedding)
        faiss_index = len(self.index_to_id)
        
        self.faiss_index.add(embedding_normalized.reshape(1, -1))
        self.id_to_index[doc_id] = faiss_index
        self.index_to_id[faiss_index] = doc_id
    
    def retrieve_document(self, doc_id: str) -> Optional[DocumentMemory]:
        """Retrieve a document from memory"""
        # Check in-memory cache first
        if doc_id in self.document_memories:
            return self.document_memories[doc_id]
        
        # Load from database
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM document_memories WHERE id = ?
        ''', (doc_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        # Load embedding from database
        cursor.execute('SELECT embedding FROM document_embeddings WHERE id = ?', (doc_id,))
        embedding_row = cursor.fetchone()
        
        if embedding_row:
            embedding = np.frombuffer(embedding_row['embedding'], dtype=np.float32)
        else:
            embedding = np.zeros(self.embedding_dim, dtype=np.float32)
        
        # Build document memory object
        doc_memory = DocumentMemory(
            id=row['id'],
            content=row['content'],
            title=row['title'],
            source_file=row['source_file'],
            embedding=embedding,
            timestamp=datetime.fromisoformat(row['timestamp']),
            document_type=row['document_type'],
            tags=json.loads(row['tags']) if row['tags'] else [],
            relationships=json.loads(row['relationships']) if row['relationships'] else {},
            metadata=json.loads(row['metadata']) if row['metadata'] else {},
            summary=row['summary'],
            page_numbers=json.loads(row['page_numbers']) if row['page_numbers'] else []
        )
        
        # Cache in memory
        self.document_memories[doc_id] = doc_memory
        return doc_memory
    
    def update_document(self, doc_id: str, **kwargs) -> bool:
        """Update an existing document"""
        doc = self.retrieve_document(doc_id)
        if not doc:
            return False
        
        # Update fields based on kwargs
        for key, value in kwargs.items():
            if hasattr(doc, key):
                setattr(doc, key, value)
        
        # Update embedding if provided
        if 'embedding' in kwargs:
            # Normalize embedding
            embedding = kwargs['embedding']
            embedding = embedding / np.linalg.norm(embedding)
            doc.embedding = embedding
            self._store_embedding(doc_id, embedding)
        
        # Store updated document in database
        self._store_in_database(doc)
        
        # Update in-memory cache
        self.document_memories[doc_id] = doc
        self.unsaved_changes[doc_id] = doc
        
        return True
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from memory system"""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Delete from both tables
        cursor.execute("DELETE FROM document_memories WHERE id = ?", (doc_id,))
        cursor.execute("DELETE FROM document_embeddings WHERE id = ?", (doc_id,))
        
        conn.commit()
        
        # Remove from in-memory cache and unsaved changes
        self.document_memories.pop(doc_id, None)
        self.unsaved_changes.pop(doc_id, None)
        
        # TODO: Update FAISS index and mappings (this is complex with FAISS)
        # For now, we'll rebuild the index when needed
        
        return True
    
    def get_all_documents(self) -> List[DocumentMemory]:
        """Get all documents (use with caution - loads all into memory)"""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM document_memories")
        
        docs = []
        for row in cursor.fetchall():
            doc = self.retrieve_document(row['id'])
            if doc:
                docs.append(doc)
        
        return docs
    
    def get_document_count(self) -> int:
        """Get count of stored documents"""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM document_memories")
        return cursor.fetchone()[0]
    
    def close(self):
        """Close database connection"""
        if hasattr(self.local, 'conn'):
            self.local.conn.close()
