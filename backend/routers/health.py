# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

"""
Health check endpoints
"""
from fastapi import APIRouter, Depends
from backend.core.dependencies import get_docmemory_system

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "service": "DocMemory API"}

@router.get("/status")
async def system_status(system = Depends(get_docmemory_system)):
    """Get system status with document count"""
    try:
        doc_count = system.get_document_count()
        return {
            "status": "active",
            "document_count": doc_count,
            "system_health": "good"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "system_health": "degraded"
        }

