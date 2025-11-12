# Aethersite (DocSynapse)

<!-- → Architecture & Build by DocSynapse-->
<!-- Intelligent by Design. Crafted for Humanity. -->

<div align="center">

![Aethersite Logo](./Aethersite.png)

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

**Aethersite** is a full-stack semantic document memory system that combines vector search with traditional databases to create an intelligent document retrieval system. Built with Next.js frontend and FastAPI backend, it provides a modern web interface for document management and semantic search.

### Why This Exists

The GitHub community gave me so much — tools, libraries, knowledge, and inspiration. Aethersite is my attempt to give back, however small.

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
Aethersite/
├── frontend/                 # Next.js frontend application
│   ├── app/                  # Next.js App Router pages
│   ├── components/           # React components
│   ├── __tests__/            # Frontend unit tests
│   ├── package.json          # Node.js dependencies
│   └── ...                   # Other Next.js files
│
├── backend/                  # FastAPI backend application
│   ├── src/                  # Core Aethersite library
│   │   ├── __init__.py
│   │   ├── docmemory_core.py
│   │   ├── search_engine.py
│   │   ├── document_processor.py
│   │   └── auto_save_load.py
│   ├── routers/              # API route handlers
│   ├── core/                 # Core backend utilities
│   ├── main.py               # FastAPI application entry point
│   └── requirements.txt      # Python dependencies
│
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── conftest.py           # Pytest configuration
│
├── docs/                     # Documentation
│   ├── architecture.md       # System architecture details
│   ├── api.md                # API documentation
│   ├── setup.md              # Setup and installation guide
│   ├── runbook.md            # Operational procedures
│   └── changelog.md          # Changelog
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
git clone https://github.com/DocSynapse/Aethersite.git
cd Aethersite

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

For detailed architecture documentation, see [docs/architecture.md](./docs/architecture.md).

---

## 📖 Documentation

- **[docs/architecture.md](./docs/architecture.md)** — System architecture and design decisions
- **[docs/api.md](./docs/api.md)** — Complete API documentation with examples
- **[docs/setup.md](./docs/setup.md)** — Installation and setup guide
- **[docs/runbook.md](./docs/runbook.md)** — Operational procedures and troubleshooting
- **[docs/changelog.md](./docs/changelog.md)** — Project changelog

---

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

---

## 🐳 Docker

### Development

```bash
docker-compose up --build
```

### Production Build

```bash
docker build -t aethersite:latest .
docker run -p 8000:8000 aethersite:latest
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

## 🤝 Contributing

Contributions are warmly welcomed! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.
