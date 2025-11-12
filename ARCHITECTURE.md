# Aethersite Architecture

**Technical Deep Dive into System Design and Implementation**

This document provides a comprehensive explanation of Aethersite's architecture, design decisions, and implementation details. It's intended for contributors, learners, and anyone curious about how semantic search systems work under the hood.

---

## Table of Contents

- [System Overview](#system-overview)
- [Core Components](#core-components)
- [Data Storage](#data-storage)
- [Search Mechanisms](#search-mechanisms)
- [Document Processing](#document-processing)
- [Performance Considerations](#performance-considerations)
- [Design Decisions](#design-decisions)

---

## System Overview

Aethersite implements a **hybrid document retrieval system** that combines:
- **Vector-based semantic search** (FAISS)
- **Traditional keyword search** (SQL LIKE queries)
- **Metadata-rich storage** (SQLite)

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    Application Interface                      │
│              AethersiteSystem (main.py)                       │
└────────────────────┬─────────────────────────────────────────┘
                     │
     ┌───────────────┼───────────────┐
     │               │               │
     ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌────────────────┐
│  Document   │ │   Search    │ │  Persistence   │
│  Processor  │ │   Engine    │ │   Manager      │
│             │ │             │ │                │
│ - Parsing   │ │ - Semantic  │ │ - Auto-save    │
│ - Chunking  │ │ - Keyword   │ │ - Backup       │
│ - Embedding │ │ - Hybrid    │ │ - Recovery     │
└──────┬──────┘ └──────┬──────┘ └───────┬────────┘
       │               │                 │
       └───────────────┼─────────────────┘
                       ▼
        ┌──────────────────────────────┐
        │      AethersiteCore           │
        │   (Core Memory Management)    │
        │                               │
        │  ┌─────────┐  ┌────────────┐ │
        │  │ SQLite  │  │   FAISS    │ │
        │  │Database │  │Vector Index│ │
        │  └─────────┘  └────────────┘ │
        │                               │
        │  ┌──────────────────────────┐│
        │  │   In-Memory Cache        ││
        │  └──────────────────────────┘│
        └──────────────────────────────┘
```

---

## Core Components

### 1. DocSynapseCore (`docsynapse_core.py`)

**Responsibility:** Central memory management and data persistence.

#### Key Classes

**DocumentMemory (Dataclass):**
```python
@dataclass
class DocumentMemory:
    id: str                          # UUID v4
    content: str                     # Full text content
    title: str                       # Document title
    source_file: str                 # Original file path
    embedding: np.ndarray            # 384-dim vector
    timestamp: datetime              # Creation time
    document_type: str               # pdf, docx, txt, etc.
    tags: List[str]                  # Custom tags
    relationships: Dict[str, float]  # {doc_id: similarity}
    metadata: Dict[str, Any]         # Flexible metadata
    summary: str                     # Optional summary
    page_numbers: List[int]          # For multi-page docs
```

**DocSynapseCore:**
- Manages SQLite connection and schema
- Maintains FAISS vector index
- Provides CRUD operations for documents
- Handles embedding storage and retrieval
- Implements bidirectional mapping: `doc_id ↔ FAISS index`

#### Database Schema

**Table: document_memories**
```sql
CREATE TABLE document_memories (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    source_file TEXT,
    timestamp TEXT,              -- ISO format
    document_type TEXT,
    tags TEXT,                   -- JSON array
    relationships TEXT,          -- JSON object
    metadata TEXT,               -- JSON object
    summary TEXT,
    page_numbers TEXT            -- JSON array
);
```

**Table: document_embeddings**
```sql
CREATE TABLE document_embeddings (
    id TEXT PRIMARY KEY,
    embedding BLOB,              -- numpy array as bytes
    FOREIGN KEY (id) REFERENCES document_memories(id)
);
```

#### FAISS Index Configuration

```python
embedding_dim = 384
faiss_index = faiss.IndexFlatIP(embedding_dim)
```

- **IndexFlatIP:** Inner product similarity (cosine distance for normalized vectors)
- **Why not IndexFlatL2?** Inner product is equivalent to cosine similarity when vectors are L2-normalized, which is our case
- **Trade-off:** No compression, but guarantees exact results

---

### 2. Search Engine (`search_engine.py`)

**Responsibility:** Implement semantic, keyword, and hybrid search algorithms.

#### Semantic Search Algorithm

```python
def semantic_search(query_embedding, limit=10):
    # 1. Normalize query embedding
    query_embedding = query_embedding / np.linalg.norm(query_embedding)
    
    # 2. FAISS similarity search
    scores, indices = faiss_index.search(
        query_embedding.reshape(1, -1),
        k=limit * 2  # Fetch extra for filtering
    )
    
    # 3. Retrieve documents from indices
    for score, idx in zip(scores[0], indices[0]):
        doc_id = index_to_id[idx]
        doc = retrieve_document(doc_id)
        results.append((doc, score))
    
    # 4. Optional reranking
    if rerank:
        results = apply_reranking(results)
    
    return results[:limit]
```

**Reranking Formula:**
```python
enhanced_score = (0.7 * cosine_similarity) 
               + (0.2 * recency_factor) 
               + (0.1 * metadata_richness)

recency_factor = exp(-age_in_days / 30)  # 30-day half-life
```

#### Keyword Search Algorithm

```python
def keyword_search(query, limit=10):
    # 1. SQL full-text search
    cursor.execute("""
        SELECT id, content, title 
        FROM document_memories
        WHERE content LIKE ? OR title LIKE ?
        ORDER BY LENGTH(content) ASC
        LIMIT ?
    """, (f"%{query}%", f"%{query}%", limit * 2))
    
    # 2. Calculate term frequency relevance
    for doc in results:
        term_count = doc.content.lower().count(query.lower())
        score = term_count / len(doc.content.split())
        ranked_results.append((doc, min(1.0, score)))
    
    return sorted(ranked_results, key=score, reverse=True)[:limit]
```

#### Hybrid Search Algorithm

```python
def hybrid_search(query, query_embedding, limit=10):
    # 1. Get both result sets
    semantic_results = semantic_search(query_embedding, limit * 2)
    keyword_results = keyword_search(query, limit * 2)
    
    # 2. Create score dictionaries
    semantic_dict = {doc.id: score for doc, score in semantic_results}
    keyword_dict = {doc.id: score for doc, score in keyword_results}
    
    # 3. Combine with weighted average
    all_doc_ids = set(semantic_dict.keys()) | set(keyword_dict.keys())
    
    for doc_id in all_doc_ids:
        semantic_score = semantic_dict.get(doc_id, 0.0)
        keyword_score = keyword_dict.get(doc_id, 0.0)
        
        # Weighted fusion
        combined_score = (0.7 * semantic_score) + (0.3 * keyword_score)
        combined_results.append((doc, combined_score))
    
    # 4. Sort and return
    return sorted(combined_results, key=score, reverse=True)[:limit]
```

**Why 70/30 Split?**
- Semantic search captures conceptual similarity
- Keyword search ensures exact term matches aren't missed
- 70/30 balances both, favoring semantic understanding
- Adjustable based on use case (can be parameterized)

---

### 3. Document Processor (`document_processor.py`)

**Responsibility:** Parse multiple document formats and chunk content intelligently.

#### Supported Formats

| Format | Library | Notes |
|--------|---------|-------|
| PDF | PyPDF2 + pdfminer.six | Fallback for better extraction |
| DOCX | python-docx | Includes table extraction |
| TXT | Built-in | UTF-8 with latin-1 fallback |
| CSV | pandas | Converted to string table |
| HTML | BeautifulSoup4 | Strips scripts/styles |
| RTF | Built-in | Treated as text |

#### Chunking Algorithm

```python
def create_chunks(content, max_size=1000, overlap=100):
    chunks = []
    start = 0
    
    while start < len(content):
        end = start + max_size
        
        if end < len(content):
            # Find sentence boundary
            search_start = end - overlap
            break_point = end
            
            for i in range(end - 1, search_start, -1):
                if content[i] in '.!?;':
                    if content[i+1] in ' \n\t':
                        break_point = i + 1
                        break
            
            # Ensure minimum chunk size
            if break_point == end:
                break_point = max(search_start, start + 50)
        
        chunk = content[start:break_point].strip()
        if chunk:
            chunks.append(DocumentChunk(
                content=chunk,
                chunk_index=len(chunks)
            ))
        
        start = break_point
    
    return chunks
```

**Chunking Strategy:**
1. **Target size:** 1000 characters
2. **Overlap:** 100 characters for context continuity
3. **Boundary-aware:** Breaks at sentence endings when possible
4. **Minimum size:** Ensures chunks are at least 50 chars
5. **Context preservation:** Overlap maintains semantic coherence

**Why These Parameters?**
- 1000 chars ≈ 150-200 tokens → fits well in embedding context
- 100 char overlap → maintains narrative continuity
- Sentence boundaries → prevents mid-thought splits

#### Processing Pipeline

```
File → Format Detection → Parser Selection
                               ↓
                    Content Extraction
                               ↓
                    Text Normalization
                               ↓
                    Semantic Chunking
                               ↓
                    Embedding Generation
                               ↓
                    Metadata Enrichment
                               ↓
                    Storage (SQLite + FAISS)
```

---

### 4. Persistence Manager (`auto_save_load.py`)

**Responsibility:** Automatic persistence, backup, and recovery.

#### Auto-Save Mechanism

```python
class AutoSaveThread(threading.Thread):
    def run(self):
        while not self.stop_event.is_set():
            time.sleep(save_interval)  # Default: 5 minutes
            
            if has_unsaved_changes():
                # SQLite auto-commits per operation
                # But we can trigger explicit backup
                create_backup()
                clear_unsaved_flags()
```

#### Signal Handling

```python
def graceful_shutdown(signum, frame):
    """Handle SIGTERM and SIGINT"""
    print("Graceful shutdown initiated...")
    
    # Save any pending changes
    save_all_unsaved_documents()
    
    # Close database connection
    close_database_connection()
    
    # Exit cleanly
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)
```

#### Backup Strategy

```python
def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backup_{timestamp}.zip"
    
    with zipfile.ZipFile(backup_path, 'w') as backup:
        backup.write(db_path, "document_memories.db")
        backup.write(faiss_index_path, "faiss_index.bin")
    
    # Rotate old backups (keep last 5)
    rotate_backups(max_backups=5)
```

---

## Data Storage

### Storage Architecture

```
Storage Path (./docsynapse_storage/)
├── document_memories.db        # SQLite database
├── faiss_index.bin            # (if serialized)
├── backups/
│   ├── backup_20250111_120000.zip
│   ├── backup_20250111_180000.zip
│   └── ...
```

### Data Flow

**Write Path:**
```
Document → Chunk → Embed → Store
                             ↓
                   ┌─────────┴──────────┐
                   ↓                    ↓
              [SQLite]              [FAISS]
           (metadata + text)      (vectors)
                   ↓                    ↓
              [In-Memory Cache for hot docs]
```

**Read Path:**
```
Query → Search (FAISS + SQLite)
            ↓
    Check Cache → Hit? Return
            ↓ Miss
    Load from DB → Cache → Return
```

---

## Search Mechanisms

### Search Type Comparison

| Search Type | Strengths | Weaknesses | Best For |
|-------------|-----------|------------|----------|
| **Semantic** | Conceptual matching, handles synonyms | May miss exact terms | Abstract queries |
| **Keyword** | Exact term matching, fast | No semantic understanding | Specific terms |
| **Hybrid** | Balanced, robust | Slightly slower | General purpose |

### Performance Characteristics

**FAISS IndexFlatIP:**
- **Search complexity:** O(d × n) where d=dimensions, n=documents
- **Memory usage:** ~1.5 KB per document (384 dims × 4 bytes)
- **Index build:** O(n) — simple array append
- **Exact results:** No approximation

**SQLite LIKE Query:**
- **Search complexity:** O(n) table scan
- **Optimizable:** Can add full-text search (FTS5) extension
- **Memory usage:** Minimal

---

## Performance Considerations

### Scalability Limits

**Current Implementation:**
- **Sweet spot:** 10K - 100K documents
- **Bottleneck:** FAISS flat index (linear search)
- **Memory limit:** ~6 GB for 100K docs

**Future Optimizations:**
- **FAISS IVF index:** Sub-linear search via clustering
- **Product Quantization:** 8x memory compression
- **SQLite FTS5:** Optimized full-text search

### Memory Management

```python
# In-memory cache with LRU-like behavior
if len(document_cache) > max_cache_size:
    # Evict least recently used
    oldest_id = min(cache_access_times, key=cache_access_times.get)
    del document_cache[oldest_id]
```

### Database Optimization

```sql
-- Recommended indexes
CREATE INDEX idx_timestamp ON document_memories(timestamp);
CREATE INDEX idx_document_type ON document_memories(document_type);
CREATE INDEX idx_source_file ON document_memories(source_file);
```

---

## Design Decisions

### Why SQLite?

✅ **Pros:**
- Serverless — no daemon to manage
- ACID transactions
- Cross-platform
- Battle-tested reliability
- Perfect for local-first apps

⚠️ **Cons:**
- Single-writer (not an issue for single-user)
- Not distributed (okay for POC)

**Verdict:** Ideal for the current scope and use case.

### Why FAISS IndexFlatIP?

✅ **Pros:**
- Exact results (no approximation)
- Simple implementation
- Predictable performance
- Easy to understand

⚠️ **Cons:**
- Linear search complexity
- Not optimal for >100K docs

**Verdict:** Right choice for POC. Can upgrade to IVF/PQ later if needed.

### Why Sentence Transformers?

✅ **Pros:**
- State-of-the-art embeddings
- Easy to use
- Pre-trained models
- Active community

⚠️ **Cons:**
- Model size (~80 MB for MiniLM)
- CPU inference latency

**Verdict:** Best balance of quality and ease of use.

### Why Simple Dictionary for Relationships?

✅ **Pros:**
- Simple to implement
- Low overhead
- Sufficient for POC

⚠️ **Future:**
- Can extend to NetworkX for graph queries
- Can add graph database (Neo4j) if needed
- Current implementation is a solid foundation

---

## Future Architectural Improvements

### Near-Term

1. **Add SQLite FTS5** for better keyword search
2. **Implement connection pooling** for concurrent access
3. **Add index optimization** for common queries
4. **Implement query caching** for repeated searches

### Long-Term

1. **Distributed FAISS** for horizontal scaling
2. **Graph database integration** for rich relationships
3. **Async I/O** for non-blocking operations
4. **Microservice architecture** for modularity

---

## Learning Resources

If you're new to these concepts:

- **Vector Search:** [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)
- **Embeddings:** [Sentence Transformers Guide](https://www.sbert.net/)
- **Information Retrieval:** [Introduction to Information Retrieval (Stanford)](https://nlp.stanford.edu/IR-book/)

---

## Questions?

Found something unclear? Want to propose an architectural change?

- Open an issue: [GitHub Issues](https://github.com/DocSynapse/Aethersite/issues)
- Start a discussion: [GitHub Discussions](https://github.com/DocSynapse/Aethersite/discussions)

---

*This document reflects the current implementation. As the system evolves, this architecture guide will be updated to reflect new decisions and improvements.*
