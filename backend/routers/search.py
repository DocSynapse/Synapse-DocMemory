# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

"""
Search endpoints
"""
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.core.dependencies import get_docmemory_system

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    search_type: Literal["semantic", "keyword", "hybrid"] = "hybrid"
    limit: int = 10

@router.post("/")
async def search_documents(
    request: SearchRequest,
    system = Depends(get_docmemory_system)
):
    """
    Search documents using semantic, keyword, or hybrid search
    """
    try:
        results = system.search(
            query=request.query,
            search_type=request.search_type,
            limit=request.limit
        )
        
        # Format results for API response
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.get("id", ""),
                "title": result.get("title", ""),
                "content": result.get("content", ""),
                "score": result.get("score", 0.0),
                "source_file": result.get("source_file", ""),
                "tags": result.get("tags", []),
                "timestamp": result.get("timestamp", "")
            })
        
        return {
            "query": request.query,
            "search_type": request.search_type,
            "results": formatted_results,
            "count": len(formatted_results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

