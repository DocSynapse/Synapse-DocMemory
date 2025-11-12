# DocMemory (DocSynapse)

<!-- → Architecture & Build by DocSynapse-->
<!-- Intelligent by Design. Crafted for Humanity. -->

<div align="center">

![DocMemory Logo](./DocMemory.png)

**Semantic Document Memory System with Vector Search**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 20+](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)
[![Status: POC](https://img.shields.io/badge/status-proof--of--concept-yellow.svg)]()

*Built with gratitude for the open source community* 💙

[Features](#-features) • [Quick Start](#-quick-start) • [Project Structure](#-project-structure) • [Architecture](#-architecture) • [Documentation](#-documentation) • [Contributing](#-contributing) • [License](#-license)

</div>

---

## 🌟 Overview

**DocMemory** is a full-stack semantic document memory system that combines vector search with traditional databases to create an intelligent document retrieval system. Built with Next.js frontend and FastAPI backend, it provides a modern web interface for document management and semantic search.

### Why This Exists

The GitHub community gave me so much — tools, libraries, knowledge, and inspiration. DocMemory is my attempt to give back, however small.

**We take, and we also give hands.** That's how we all grow together.

If this code helps even one person learn something new, or solves even one problem, then sharing it was worth it.

### Current Status

🟡 **Proof of Concept** — Core features work reliably, but this is an early-stage project:
- ✅ Core functionality is stable
- ✅ Full-stack scaffold complete
- ⚠️ Not production-hardened
- 🔨 Active development and improvements ongoing
- 🤝 Community contributions welcome!

---

## ✨ Features

### Currently Implemented

- **🔍 Semantic Search** — Find documents by meaning, not just keywords, using FAISS vector similarity
- **🔀 Hybrid Search** — Combines semantic understanding (70%) with keyword matching (30%) for balanced results
- **💾 Persistent Storage** — SQLite database with automatic save/load and backup rotation
- **📄 Multi-Format Support** — Process PDF, DOCX, TXT, HTML, CSV, and more
- **🧩 Smart Chunking** — Intelligent content splitting with overlap for context preservation
- **🏷️ Tagging System** — Organize and filter documents with custom tags
- **🔗 Document Relationships** — Find related documents based on semantic similarity
- **⚡ Fast Retrieval** — FAISS-powered vector indexing for millisecond-scale search
- **🔄 Auto-Save** — Thread-safe automatic persistence with graceful shutdown handlers
- **🌐 Modern Web Interface** — Next.js frontend with responsive design
- **🚀 RESTful API** — FastAPI backend with OpenAPI documentation
- **🐳 Docker Support** — Containerized deployment with docker-compose
- **🧪 Testing Infrastructure** — Unit and integration tests
- **🔄 CI/CD** — GitHub Actions for automated testing

### Architecture Highlights

```
Frontend: Next.js 14 + TypeScript + Tailwind CSS
Backend: FastAPI + Python 3.9+
Storage: SQLite + FAISS + In-Memory Cache
Embeddings: Sentence Transformers (all-MiniLM-L6-v2, 384-dim)
Search: Inner product similarity (cosine distance)
Chunking: 1000 chars with 100 char overlap, sentence-aware
```

---

## 📁 Project Structure

```
DocMemory/
├── frontend/                 # Next.js frontend application
│   ├── app/                  # Next.js App Router pages
│   │   ├── layout.tsx        # Root layout component
│   │   ├── page.tsx          # Home page
│   │   └── globals.css       # Global styles
│   ├── components/           # React components
│   │   ├── SearchBar.tsx     # Search input component
│   │   ├── DocumentList.tsx  # Document list display
│   │   └── UploadArea.tsx    # File upload component
│   ├── __tests__/            # Frontend unit tests
│   ├── package.json          # Node.js dependencies
│   ├── next.config.js        # Next.js configuration
│   ├── tsconfig.json         # TypeScript configuration
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   └── jest.config.js        # Jest test configuration
│
├── backend/                  # FastAPI backend application
│   ├── routers/              # API route handlers
│   │   ├── health.py         # Health check endpoints
│   │   ├── search.py         # Search endpoints
│   │   └── documents.py      # Document CRUD endpoints
│   ├── core/                 # Core backend utilities
│   │   ├── config.py         # Application configuration
│   │   └── dependencies.py   # Dependency injection
│   ├── main.py               # FastAPI application entry point
│   └── requirements.txt      # Python dependencies
│
├── src/                      # Core DocMemory library
│   ├── docmemory_core.py     # Core memory management
│   ├── search_engine.py      # Search algorithms
│   ├── document_processor.py # Document parsing and chunking
│   └── auto_save_load.py     # Persistence management
│
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   │   └── test_search_engine.py
│   ├── integration/          # Integration tests
│   │   └── test_api.py
│   └── conftest.py           # Pytest configuration
│
├── docs/                     # Documentation
│   ├── architecture.md       # System architecture details
│   ├── api.md                # API documentation
│   ├── setup.md              # Setup and installation guide
│   └── runbook.md            # Operational procedures
│
├── .github/                  # GitHub configuration
│   └── workflows/
│       └── ci.yml            # CI/CD pipeline
│
├── main.py                   # Legacy CLI entry point
├── requirements.txt          # Core Python dependencies
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose configuration
├── pytest.ini               # Pytest configuration
└── README.md                 # This file
```

### File Descriptions

#### Frontend Files

- **`frontend/app/layout.tsx`**: Root layout with metadata configuration
- **`frontend/app/page.tsx`**: Main home page with search and document display
- **`frontend/components/SearchBar.tsx`**: Search input component with query handling
- **`frontend/components/DocumentList.tsx`**: Component for displaying search results
- **`frontend/components/UploadArea.tsx`**: File upload interface with drag-and-drop
- **`frontend/package.json`**: Node.js dependencies and scripts
- **`frontend/next.config.js`**: Next.js configuration (TODO: Configure production API URL)
- **`frontend/tsconfig.json`**: TypeScript compiler configuration
- **`frontend/tailwind.config.js`**: Tailwind CSS theme configuration (TODO: Customize theme)
- **`frontend/jest.config.js`**: Jest test configuration (TODO: Configure coverage thresholds)

#### Backend Files

- **`backend/main.py`**: FastAPI application with CORS and route registration
- **`backend/routers/health.py`**: Health check and system status endpoints
- **`backend/routers/search.py`**: Search API endpoints (semantic, keyword, hybrid)
- **`backend/routers/documents.py`**: Document upload, list, get, and related documents endpoints (TODO: Implement pagination)
- **`backend/core/config.py`**: Application settings and environment variables (TODO: Add database URL, Redis URL, auth settings)
- **`backend/core/dependencies.py`**: Dependency injection for DocMemory system instance
- **`backend/requirements.txt`**: Backend Python dependencies (TODO: Add auth, database, Redis dependencies)

#### Core Library Files

- **`src/docmemory_core.py`**: Core memory management with SQLite and FAISS
- **`src/search_engine.py`**: Search algorithms (semantic, keyword, hybrid)
- **`src/document_processor.py`**: Document parsing, chunking, and embedding
- **`src/auto_save_load.py`**: Automatic persistence and backup management

#### Test Files

- **`tests/unit/test_search_engine.py`**: Unit tests for search functionality (TODO: Add more test cases)
- **`tests/integration/test_api.py`**: Integration tests for API endpoints (TODO: Add more tests)
- **`tests/conftest.py`**: Shared pytest fixtures and configuration
- **`pytest.ini`**: Pytest configuration with coverage settings

#### Infrastructure Files

- **`Dockerfile`**: Multi-stage Docker build for production (TODO: Add production optimizations, healthcheck, non-root user)
- **`docker-compose.yml`**: Docker Compose configuration for development (TODO: Add PostgreSQL, Redis, healthchecks)
- **`frontend/Dockerfile`**: Frontend-specific Dockerfile for Next.js
- **`.dockerignore`**: Files to exclude from Docker builds
- **`.github/workflows/ci.yml`**: GitHub Actions CI/CD pipeline (TODO: Add coverage upload, Docker push)

#### Documentation Files

- **`docs/architecture.md`**: Detailed system architecture and design decisions
- **`docs/api.md`**: Complete API documentation with examples
- **`docs/setup.md`**: Installation and setup instructions
- **`docs/runbook.md`**: Operational procedures and troubleshooting guide

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 20+
- npm 9+
- Docker (optional, for containerized deployment)

### Installation

#### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/docmemory.git
cd docmemory

# Start with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

#### Option 2: Local Development

**Backend Setup:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt

# Run backend
cd backend
uvicorn main:app --reload
```

**Frontend Setup:**
```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev
```

### First Steps

1. **Access the Web Interface**: http://localhost:3000
2. **Upload a Document**: Use the upload area or API
3. **Search Documents**: Try semantic search queries
4. **Explore API Docs**: http://localhost:8000/docs

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                    │
│              React Components + API Client              │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────┐
│                  Backend (FastAPI)                       │
│              REST API + Business Logic                   │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────────┐ ┌─────────┐ ┌──────────────┐
│  Document    │ │ Search  │ │ Persistence  │
│  Processor   │ │ Engine  │ │ Manager      │
└──────┬───────┘ └────┬────┘ └──────┬───────┘
       │              │              │
       └──────────────┼──────────────┘
                      ▼
         ┌────────────────────────┐
         │   Core Memory System   │
         │  (SQLite + FAISS)       │
         └────────────────────────┘
```

For detailed architecture documentation, see [docs/architecture.md](./docs/architecture.md).

---

## 📖 Documentation

- **[docs/architecture.md](./docs/architecture.md)** — System architecture and design decisions
- **[docs/api.md](./docs/api.md)** — Complete API documentation with examples
- **[docs/setup.md](./docs/setup.md)** — Installation and setup guide
- **[docs/runbook.md](./docs/runbook.md)** — Operational procedures and troubleshooting
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** — Original architecture documentation

---

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_search_engine.py -v
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

---

## 🐳 Docker

### Development

```bash
docker-compose up --build
```

### Production Build

```bash
docker build -t docmemory:latest .
docker run -p 8000:8000 docmemory:latest
```

---

## 🔄 CI/CD

GitHub Actions workflow runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

**Workflow Steps:**
1. Backend tests (unit + integration)
2. Frontend tests and linting
3. Docker build verification

See [.github/workflows/ci.yml](./.github/workflows/ci.yml) for details.

---

## 🛠️ Development

### Code Style

**Python:**
- Follow PEP 8
- Use Black for formatting (TODO: Add pre-commit hooks)
- Type hints recommended

**TypeScript:**
- ESLint configuration included
- Prettier recommended (TODO: Add Prettier config)

### Adding Features

1. Create feature branch
2. Implement feature with tests
3. Update documentation
4. Submit pull request

---

## 🤝 Contributing

Contributions are warmly welcomed! Whether it's:
- 🐛 Bug reports
- 💡 Feature suggestions
- 📝 Documentation improvements
- 🔧 Code contributions

Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Areas Where Help is Needed

- [ ] Production error handling and edge cases
- [ ] Performance benchmarking suite
- [ ] More document format support (Markdown, LaTeX, etc.)
- [ ] Graph-based relationship visualization
- [ ] Distributed deployment support
- [ ] Authentication and authorization
- [ ] Database migration to PostgreSQL
- [ ] Redis caching implementation

---

## 🗺️ Roadmap

### Near Term (Next Version)

- [ ] Complete test coverage
- [ ] Production optimizations
- [ ] Authentication system
- [ ] Database migration to PostgreSQL
- [ ] Redis caching layer
- [ ] Performance benchmarking

### Future Vision

- [ ] True graph-based neural connections (NetworkX integration)
- [ ] Multi-modal support (images, audio)
- [ ] Distributed FAISS for scaling
- [ ] Real-time collaborative features
- [ ] Advanced analytics dashboard

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

```
MIT License - Free to use, modify, and distribute.
Built with ❤️ for the community.
```

---

## 🙏 Acknowledgments

This project wouldn't exist without:

- **FAISS** — Facebook AI's vector similarity library
- **Sentence Transformers** — Hugging Face's embedding models
- **SQLite** — The most deployed database in the world
- **Next.js** — React framework for production
- **FastAPI** — Modern Python web framework
- **The entire open source community** — For countless tools and inspiration

Special thanks to everyone who contributes, reports issues, or simply uses this project. You make sharing worthwhile. 🙌

---

## 📧 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/docmemory/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/docmemory/discussions)
- **Email:** your.email@example.com

---

<div align="center">

**Built with 🧠 by the DocMemory Community**

*Architecture & Build by DocSynapse • Intelligent by Design. Crafted for Humanity.*

[⭐ Star this repo](https://github.com/yourusername/docmemory) if you find it useful!

</div>
