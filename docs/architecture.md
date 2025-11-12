# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

# DocMemory Architecture

## System Overview

DocMemory is a full-stack semantic document memory system built with:
- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Backend**: FastAPI (Python) with RESTful API
- **Storage**: SQLite + FAISS for vector search
- **Deployment**: Docker containers with docker-compose

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                         │
│                    (Next.js + React)                          │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Search UI  │  │  Upload UI   │  │ Document List│     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            │                                  │
│                    ┌───────▼────────┐                        │
│                    │  API Client    │                        │
│                    │  (Axios)       │                        │
│                    └───────┬────────┘                        │
└────────────────────────────┼──────────────────────────────────┘
                             │ HTTP/REST
┌────────────────────────────┼──────────────────────────────────┐
│                    ┌──────▼────────┐                        │
│                    │  FastAPI      │                        │
│                    │  Backend      │                        │
│                    └───────┬────────┘                        │
│                            │                                  │
│         ┌──────────────────┼──────────────────┐              │
│         │                  │                  │              │
│  ┌──────▼──────┐  ┌───────▼──────┐  ┌───────▼──────┐      │
│  │  Search     │  │  Documents   │  │   Health     │      │
│  │  Router     │  │  Router      │  │   Router     │      │
│  └──────┬──────┘  └───────┬──────┘  └──────────────┘      │
│         │                  │                                  │
│         └──────────┬───────┘                                  │
│                    │                                          │
│         ┌──────────▼──────────┐                              │
│         │  DocMemory System    │                              │
│         │  (Core Logic)         │                              │
│         └──────────┬───────────┘                              │
└────────────────────┼──────────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────▼────┐ ┌───▼────┐ ┌───▼────┐
    │ SQLite  │ │ FAISS  │ │  Cache │
    │  DB     │ │ Index  │ │        │
    └─────────┘ └────────┘ └────────┘
```

## Component Details

### Frontend Components

1. **SearchBar** (`frontend/components/SearchBar.tsx`)
   - Handles user search queries
   - Supports semantic, keyword, and hybrid search types

2. **DocumentList** (`frontend/components/DocumentList.tsx`)
   - Displays search results
   - Shows document metadata and scores

3. **UploadArea** (`frontend/components/UploadArea.tsx`)
   - File upload interface
   - Supports drag-and-drop

### Backend Components

1. **API Routers** (`backend/routers/`)
   - `health.py`: Health check endpoints
   - `search.py`: Search functionality
   - `documents.py`: Document CRUD operations

2. **Core System** (`src/`)
   - `docmemory_core.py`: Core memory management
   - `search_engine.py`: Search algorithms
   - `document_processor.py`: Document parsing and chunking
   - `auto_save_load.py`: Persistence management

### Data Flow

**Document Upload:**
```
File Upload → FastAPI → Document Processor → Chunker → Embedder → 
SQLite (metadata) + FAISS (vectors) → Response
```

**Search Query:**
```
Query → FastAPI → Search Engine → 
FAISS (semantic) + SQLite (keyword) → Merge Results → Response
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **State Management**: React Query (TanStack Query)
- **Testing**: Jest + React Testing Library

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.9+
- **API**: RESTful
- **Storage**: SQLite + FAISS
- **Embeddings**: Sentence Transformers
- **Testing**: Pytest + httpx

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: GitHub Actions
- **Version Control**: Git

## Scalability Considerations

### Current Limitations
- SQLite: Single-writer, suitable for single-user or low-concurrency
- FAISS IndexFlatIP: Linear search, suitable for <100K documents

### Future Improvements
- **Database**: Migrate to PostgreSQL for multi-user support
- **Vector Search**: Upgrade to FAISS IVF for sub-linear search
- **Caching**: Add Redis for query caching
- **Load Balancing**: Add nginx for frontend serving
- **Authentication**: Implement JWT-based auth

## Security Considerations

### TODO: Implement Security Features
- [ ] Authentication and authorization
- [ ] Rate limiting
- [ ] Input validation and sanitization
- [ ] CORS configuration for production
- [ ] HTTPS/TLS encryption
- [ ] Secrets management
- [ ] SQL injection prevention (already handled by SQLite parameterization)

## Performance Optimization

### Current Optimizations
- FAISS vector indexing for fast similarity search
- In-memory caching for frequently accessed documents
- Chunked document processing for large files

### TODO: Additional Optimizations
- [ ] Query result caching with Redis
- [ ] Database connection pooling
- [ ] CDN for static assets
- [ ] Image optimization for frontend
- [ ] Code splitting for frontend bundles

## Deployment Architecture

### Development
```
Frontend (localhost:3000) → Backend (localhost:8000) → SQLite + FAISS
```

### Production (Docker)
```
Frontend Container → Backend Container → Volume (SQLite + FAISS)
```

### Production (Recommended)
```
Nginx → Frontend (Next.js) → Backend (FastAPI) → PostgreSQL + FAISS
```

## Monitoring and Observability

### TODO: Add Monitoring
- [ ] Application metrics (Prometheus)
- [ ] Log aggregation (ELK Stack or similar)
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring (APM)
- [ ] Health check endpoints (already implemented)

## Development Workflow

1. **Local Development**
   ```bash
   # Backend
   cd backend && uvicorn main:app --reload
   
   # Frontend
   cd frontend && npm run dev
   ```

2. **Testing**
   ```bash
   # Backend tests
   pytest tests/
   
   # Frontend tests
   cd frontend && npm test
   ```

3. **Docker Development**
   ```bash
   docker-compose up --build
   ```

## References

- [ARCHITECTURE.md](../ARCHITECTURE.md) - Original architecture documentation
- [API.md](./api.md) - API documentation
- [SETUP.md](./setup.md) - Setup instructions

