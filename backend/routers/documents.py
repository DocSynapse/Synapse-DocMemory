# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

"""
Document management endpoints
"""
import os
import tempfile
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from backend.core.dependencies import get_docmemory_system

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = None,
    tags: Optional[str] = None,
    system = Depends(get_docmemory_system)
):
    """
    Upload a document to the system
    """
    # Save uploaded file temporarily
    temp_path = None
    try:
        # Create temporary file
        suffix = os.path.splitext(file.filename)[1] if file.filename else '.txt'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            temp_path = tmp_file.name
            content = await file.read()
            tmp_file.write(content)
        
        # Parse tags
        tag_list = tags.split(',') if tags else []
        
        # Add document to system
        doc_ids = system.add_document_from_file(
            file_path=temp_path,
            title=title or file.filename,
            tags=tag_list
        )
        
        return {
            "success": True,
            "document_ids": doc_ids,
            "count": len(doc_ids),
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

@router.get("/")
async def list_documents(
    limit: int = 50,
    offset: int = 0,
    system = Depends(get_docmemory_system)
):
    """
    List documents in the system
    TODO: Implement pagination properly
    """
    # TODO: Implement proper document listing with pagination
    return {
        "documents": [],
        "total": system.get_document_count(),
        "limit": limit,
        "offset": offset
    }

@router.get("/{doc_id}")
async def get_document(
    doc_id: str,
    system = Depends(get_docmemory_system)
):
    """
    Get a specific document by ID
    """
    try:
        doc = system.get_document(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "tags": doc.tags,
            "document_type": doc.document_type,
            "timestamp": doc.timestamp.isoformat() if doc.timestamp else None,
            "source_file": doc.source_file
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{doc_id}/related")
async def get_related_documents(
    doc_id: str,
    limit: int = 5,
    system = Depends(get_docmemory_system)
):
    """
    Get documents related to a specific document
    """
    try:
        related = system.get_related_documents(doc_id, limit=limit)
        return {
            "document_id": doc_id,
            "related": related
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

