<!-- → Architecture & Build by DocSynapse-->
<!-- Intelligent by Design. Crafted for Humanity. -->

# Aethersite API Documentation

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.docmemory.example.com` (TODO: Configure)

## Authentication

Currently, the API does not require authentication. 

**TODO**: Implement JWT-based authentication for production use.

## Endpoints

### Health Check

#### GET `/api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Aethersite API"
}
```

#### GET `/api/status`

Get system status with document count.

**Response:**
```json
{
  "status": "active",
  "document_count": 42,
  "system_health": "good"
}
```

### Search

#### POST `/api/search/`

Search documents using semantic, keyword, or hybrid search.

**Request Body:**
```json
{
  "query": "machine learning concepts",
  "search_type": "hybrid",
  "limit": 10
}
```

**Parameters:**
- `query` (string, required): Search query text
- `search_type` (string, optional): One of `"semantic"`, `"keyword"`, or `"hybrid"`. Default: `"hybrid"`
- `limit` (integer, optional): Maximum number of results. Default: `10`

**Response:**
```json
{
  "query": "machine learning concepts",
  "search_type": "hybrid",
  "results": [
    {
      "id": "doc-uuid-123",
      "title": "AI Research Paper",
      "content": "Machine learning is a subset of artificial intelligence...",
      "score": 0.892,
      "source_file": "/path/to/document.pdf",
      "tags": ["AI", "research"],
      "timestamp": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

### Documents

#### POST `/api/documents/upload`

Upload a document to the system.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `file` (file, required): Document file (PDF, DOCX, TXT)
  - `title` (string, optional): Document title
  - `tags` (string, optional): Comma-separated tags

**Response:**
```json
{
  "success": true,
  "document_ids": ["doc-uuid-1", "doc-uuid-2"],
  "count": 2,
  "filename": "document.pdf"
}
```

#### GET `/api/documents/`

List documents in the system.

**Query Parameters:**
- `limit` (integer, optional): Maximum number of results. Default: `50`
- `offset` (integer, optional): Pagination offset. Default: `0`

**Response:**
```json
{
  "documents": [],
  "total": 42,
  "limit": 50,
  "offset": 0
}
```

**TODO**: Implement proper document listing with pagination.

#### GET `/api/documents/{doc_id}`

Get a specific document by ID.

**Path Parameters:**
- `doc_id` (string, required): Document UUID

**Response:**
```json
{
  "id": "doc-uuid-123",
  "title": "AI Research Paper",
  "content": "Full document content...",
  "tags": ["AI", "research"],
  "document_type": "pdf",
  "timestamp": "2024-01-15T10:30:00",
  "source_file": "/path/to/document.pdf"
}
```

#### GET `/api/documents/{doc_id}/related`

Get documents related to a specific document.

**Path Parameters:**
- `doc_id` (string, required): Document UUID

**Query Parameters:**
- `limit` (integer, optional): Maximum number of related documents. Default: `5`

**Response:**
```json
{
  "document_id": "doc-uuid-123",
  "related": [
    {
      "id": "doc-uuid-456",
      "title": "Related Document",
      "score": 0.85
    }
  ]
}
```

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message description"
}
```

### Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Example Error Response

```json
{
  "detail": "Upload failed: File format not supported"
}
```

## Rate Limiting

**TODO**: Implement rate limiting for production.

## CORS

CORS is configured for the following origins:
- `http://localhost:3000`
- `http://localhost:3001`
- `http://127.0.0.1:3000`

**TODO**: Configure production CORS origins.

## Interactive API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Examples

### cURL Examples

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

**Search:**
```bash
curl -X POST http://localhost:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "search_type": "hybrid", "limit": 10}'
```

**Upload Document:**
```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@document.pdf" \
  -F "title=My Document" \
  -F "tags=research,AI"
```

### JavaScript/TypeScript Example

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

// Search
const searchResults = await api.post('/api/search/', {
  query: 'machine learning',
  search_type: 'hybrid',
  limit: 10
});

// Upload
const formData = new FormData();
formData.append('file', file);
formData.append('title', 'My Document');
formData.append('tags', 'research,AI');

const uploadResult = await api.post('/api/documents/upload', formData);
```

### Python Example

```python
import requests

# Search
response = requests.post(
    'http://localhost:8000/api/search/',
    json={
        'query': 'machine learning',
        'search_type': 'hybrid',
        'limit': 10
    }
)
results = response.json()

# Upload
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    data = {
        'title': 'My Document',
        'tags': 'research,AI'
    }
    response = requests.post(
        'http://localhost:8000/api/documents/upload',
        files=files,
        data=data
    )
```

## Versioning

Current API version: `1.0.0`

**TODO**: Implement API versioning strategy (e.g., `/api/v1/`).

## Changelog

### v1.0.0 (Current)
- Initial API release
- Health check endpoints
- Search functionality
- Document upload and retrieval
- Related documents endpoint

## Support

For API issues or questions:
- GitHub Issues: [TODO: Add link]
- Documentation: [TODO: Add link]
