# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_list_documents_endpoint():
    """Test list documents endpoint"""
    response = client.get("/api/documents/")
    assert response.status_code == 200
    assert "documents" in response.json()

def test_upload_endpoint():
    """Test document upload endpoint"""
    with open("README.md", "rb") as f:
        response = client.post(
            "/api/documents/upload",
            files={"file": ("README.md", f, "text/markdown")},
        )
    assert response.status_code == 200
    assert "document_ids" in response.json()
