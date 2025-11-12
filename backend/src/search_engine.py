"""
Aethersite - Search and Retrieval Algorithms
Advanced semantic search and retrieval functionality
"""
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from .docmemory_core import AethersiteCore, DocumentMemory

class SemanticSearchEngine:
    """Advanced semantic search engine for document retrieval"""
    
    def __init__(self, core_memory: AethersiteCore):
        self.core_memory = core_memory
        self.search_history = []
        self.max_search_history = 100
    
    def semantic_search(self, 
                       query_embedding: np.ndarray, 
                       limit: int = 10,
                       filters: Dict[str, any] = None,
                       rerank: bool = True) -> List[Tuple[DocumentMemory, float]]:
        """Perform semantic search using vector similarity"""
        # Normalize query embedding
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        # Perform FAISS search
        if self.core_memory.faiss_index.ntotal == 0:
            return []  # No documents to search
        
        # Search in FAISS index
        scores, indices = self.core_memory.faiss_index.search(
            query_embedding.reshape(1, -1).astype(np.float32), 
            min(limit * 2, self.core_memory.faiss_index.ntotal)  # Search for more to allow filtering
        )
        
        # Get document IDs from indices
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and idx in self.core_memory.index_to_id:  # Valid index
                doc_id = self.core_memory.index_to_id[idx]
                
                # Retrieve document
                doc = self.core_memory.retrieve_document(doc_id)
                if doc:
                    # Apply filters if provided
                    if filters and not self._apply_filters(doc, filters):
                        continue
                    
                    results.append((doc, float(score)))
        
        # Sort by score (similarity) - higher is better
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Apply reranking if requested
        if rerank:
            results = self._rerank_results(query_embedding, results)
        
        return results[:limit]
    
    def _apply_filters(self, doc: DocumentMemory, filters: Dict[str, any]) -> bool:
        """Apply filters to search results"""
        for key, value in filters.items():
            if key == 'document_type' and doc.document_type != value:
                return False
            elif key == 'tags' and not any(tag in doc.tags for tag in value):
                return False
            elif key == 'source_file' and doc.source_file != value:
                return False
            # Add more filter types as needed
        return True
    
    def _rerank_results(self, query_embedding: np.ndarray, 
                       results: List[Tuple[DocumentMemory, float]]) -> List[Tuple[DocumentMemory, float]]:
        """Apply reranking to improve search quality"""
        # In a more sophisticated system, this would use cross-encoder models
        # or other reranking techniques. For now, we'll apply a simple enhancement
        # that considers factors like document recency and metadata
        
        enhanced_results = []
        for doc, score in results:
            # Apply recency boost for recent documents
            time_factor = self._calculate_recency_factor(doc.timestamp)
            
            # Apply content length normalization to avoid bias toward longer docs
            length_factor = min(1.0, len(doc.content) / 1000)  # Normalize against 1000 chars
            
            # Apply metadata-based scoring
            metadata_factor = self._calculate_metadata_factor(doc)
            
            # Combine scores
            enhanced_score = (0.7 * score) + (0.2 * time_factor) + (0.1 * metadata_factor)
            
            enhanced_results.append((doc, enhanced_score))
        
        # Sort by enhanced score
        enhanced_results.sort(key=lambda x: x[1], reverse=True)
        return enhanced_results
    
    def _calculate_recency_factor(self, timestamp) -> float:
        """Calculate recency factor based on document age"""
        from datetime import datetime, timedelta
        
        now = datetime.now()
        age = now - timestamp
        
        # Return higher scores for more recent documents (up to 1.0)
        # with exponential decay over time
        age_in_days = age.total_seconds() / (24 * 3600)
        recency_score = np.exp(-age_in_days / 30)  # 30-day half-life
        return min(1.0, recency_score)
    
    def _calculate_metadata_factor(self, doc: DocumentMemory) -> float:
        """Calculate score based on document metadata"""
        # Higher scores for documents with more metadata or tags
        meta_score = 0.1 * len(doc.tags)  # 0.1 per tag
        meta_score += 0.2 * len(doc.metadata)  # 0.2 per metadata item
        return min(1.0, meta_score)
    
    def keyword_search(self, query: str, limit: int = 10) -> List[Tuple[DocumentMemory, float]]:
        """Traditional keyword-based search"""
        # This would normally use full-text search like Elasticsearch
        # For now, we'll do a simple substring match with SQLite
        
        cursor = self.core_memory.conn.cursor()
        
        # Simple full-text search using SQLite LIKE
        search_term = f"%{query}%"
        cursor.execute('''
            SELECT id, content, title FROM document_memories 
            WHERE content LIKE ? OR title LIKE ?
            ORDER BY LENGTH(content) ASC
            LIMIT ?
        ''', (search_term, search_term, limit*2))  # Get more results for relevance scoring
        
        results = []
        for row in cursor.fetchall():
            doc_id = row['id']
            doc = self.core_memory.retrieve_document(doc_id)
            if doc:
                # Simple relevance score based on query term frequency
                query_lower = query.lower()
                content_lower = doc.content.lower()
                
                term_count = content_lower.count(query_lower)
                if ' ' in query:
                    # For multi-word queries, also check whole phrase
                    term_count += content_lower.count(query_lower) * 2
                
                score = term_count / len(content_lower.split())  # Normalize by document length
                results.append((doc, min(1.0, score)))
        
        # Sort by score
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]
    
    def hybrid_search(self, 
                     query: str,
                     query_embedding: np.ndarray,
                     semantic_weight: float = 0.7,
                     keyword_weight: float = 0.3,
                     limit: int = 10) -> List[Tuple[DocumentMemory, float]]:
        """Combine semantic and keyword search results"""
        # Get semantic search results
        semantic_results = self.semantic_search(query_embedding, limit=limit*2)
        
        # Get keyword search results
        keyword_results = self.keyword_search(query, limit=limit*2)
        
        # Create result dictionaries for easy access
        semantic_dict = {doc.id: score for doc, score in semantic_results}
        keyword_dict = {doc.id: score for doc, score in keyword_results}
        
        # Combine scores using weighted average
        combined_results = []
        all_doc_ids = set(semantic_dict.keys()) | set(keyword_dict.keys())
        
        for doc_id in all_doc_ids:
            semantic_score = semantic_dict.get(doc_id, 0.0)
            keyword_score = keyword_dict.get(doc_id, 0.0)
            
            # Normalize scores to 0-1 range if needed
            combined_score = (semantic_weight * semantic_score) + (keyword_weight * keyword_score)
            
            # Retrieve document
            doc = self.core_memory.retrieve_document(doc_id)
            if doc:
                combined_results.append((doc, combined_score))
        
        # Sort by combined score
        combined_results.sort(key=lambda x: x[1], reverse=True)
        return combined_results[:limit]
    
    def search_by_tags(self, tags: List[str], limit: int = 10) -> List[DocumentMemory]:
        """Search documents by tags"""
        cursor = self.core_memory.conn.cursor()
        
        # Build query to search for documents containing any of the tags
        placeholders = ','.join(['?' for _ in tags])
        query = f'''
            SELECT * FROM document_memories 
            WHERE tags LIKE ?
            LIMIT ?
        '''
        
        results = []
        for tag in tags:
            cursor.execute(query, (f'%{tag}%', limit))
            for row in cursor.fetchall():
                doc = self.core_memory.retrieve_document(row['id'])
                if doc and doc not in [r[0] for r in results]:
                    results.append((doc, 1.0))  # Score for tag match
        
        # Sort by document ID to provide consistent results
        results.sort(key=lambda x: x[0].id)
        return [doc for doc, _ in results[:limit]]
    
    def get_related_documents(self, doc_id: str, limit: int = 5) -> List[Tuple[DocumentMemory, float]]:
        """Find documents related to a given document"""
        doc = self.core_memory.retrieve_document(doc_id)
        if not doc:
            return []
        
        # For now, return documents with similar tags or from same source
        # In a more advanced system, this would use the relationships field
        # or perform semantic similarity search with the document's embedding
        
        related_docs = []
        
        # Find documents with similar tags
        for tag in doc.tags:
            tag_results = self.search_by_tags([tag], limit=limit)
            for related_doc in tag_results:
                if related_doc.id != doc_id and related_doc not in [r[0] for r in related_docs]:
                    # Calculate similarity based on embedding
                    similarity = np.dot(doc.embedding, related_doc.embedding)
                    related_docs.append((related_doc, similarity))
        
        # Find documents from same source file
        cursor = self.core_memory.conn.cursor()
        cursor.execute('''
            SELECT id FROM document_memories 
            WHERE source_file = ? AND id != ?
            LIMIT ?
        ''', (doc.source_file, doc_id, limit))
        
        for row in cursor.fetchall():
            related_doc = self.core_memory.retrieve_document(row['id'])
            if related_doc and related_doc not in [r[0] for r in related_docs]:
                similarity = np.dot(doc.embedding, related_doc.embedding)
                related_docs.append((related_doc, similarity))
        
        # Sort by similarity score
        related_docs.sort(key=lambda x: x[1], reverse=True)
        return related_docs[:limit]

class AethersiteSearchSystem:
    """Main search system integrating with Aethersite"""
    
    def __init__(self, docmemory_system):
        self.docmemory_system = docmemory_system
        self.search_engine = SemanticSearchEngine(docmemory_system.core_memory)
    
    def search(self, 
               query: str, 
               query_embedding: np.ndarray = None,
               search_type: str = "hybrid",  # semantic, keyword, hybrid
               limit: int = 10,
               filters: Dict[str, any] = None) -> List[Dict[str, any]]:
        """Main search method"""
        results = []
        
        if search_type == "semantic" and query_embedding is not None:
            search_results = self.search_engine.semantic_search(
                query_embedding, limit=limit, filters=filters
            )
        elif search_type == "keyword":
            search_results = self.search_engine.keyword_search(query, limit=limit)
        elif search_type == "hybrid" and query_embedding is not None:
            search_results = self.search_engine.hybrid_search(
                query, query_embedding, limit=limit
            )
        else:
            # Default to semantic if embedding provided, otherwise keyword
            if query_embedding is not None:
                search_results = self.search_engine.semantic_search(
                    query_embedding, limit=limit, filters=filters
                )
            else:
                search_results = self.search_engine.keyword_search(query, limit=limit)
        
        # Format results
        for doc, score in search_results:
            results.append({
                'id': doc.id,
                'title': doc.title,
                'content': doc.content[:200] + "..." if len(doc.content) > 200 else doc.content,
                'source_file': doc.source_file,
                'document_type': doc.document_type,
                'tags': doc.tags,
                'timestamp': doc.timestamp.isoformat(),
                'score': float(score),
                'summary': doc.summary,
                'page_numbers': doc.page_numbers
            })
        
        return results
    
    def find_related_documents(self, doc_id: str, limit: int = 5) -> List[Dict[str, any]]:
        """Find documents related to a specific document"""
        related_docs = self.search_engine.get_related_documents(doc_id, limit)
        
        results = []
        for doc, score in related_docs:
            results.append({
                'id': doc.id,
                'title': doc.title,
                'content': doc.content[:150] + "..." if len(doc.content) > 150 else doc.content,
                'source_file': doc.source_file,
                'score': float(score)
            })
        
        return results
    
    def search_by_tags(self, tags: List[str], limit: int = 10) -> List[Dict[str, any]]:
        """Search documents by tags"""
        docs = self.search_engine.search_by_tags(tags, limit)
        
        results = []
        for doc in docs:
            results.append({
                'id': doc.id,
                'title': doc.title,
                'content': doc.content[:150] + "..." if len(doc.content) > 150 else doc.content,
                'source_file': doc.source_file,
                'tags': doc.tags
            })
        
        return results