# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

# DocMemory Setup Guide

## Prerequisites

### System Requirements

- **Python**: 3.9 or higher
- **Node.js**: 20.x or higher
- **npm**: 9.x or higher
- **Docker**: 20.x or higher (optional, for containerized deployment)
- **Git**: Latest version

### Operating System

- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian 11+, or similar)

## Installation Methods

### Method 1: Local Development Setup

#### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/docmemory.git
cd docmemory
```

#### Step 2: Backend Setup

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

#### Step 3: Frontend Setup

```bash
cd frontend
npm install
cd ..
```

#### Step 4: Environment Configuration

Create `.env` file in the root directory:

```bash
# Backend
STORAGE_PATH=./docmemory_storage/
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Frontend (create frontend/.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**TODO**: Add more environment variables as needed (database URLs, API keys, etc.)

#### Step 5: Run Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Method 2: Docker Setup

#### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/docmemory.git
cd docmemory
```

#### Step 2: Build and Run with Docker Compose

```bash
docker-compose up --build
```

This will start:
- Backend API on port 8000
- Frontend on port 3000

#### Step 3: Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Method 3: Production Deployment

**TODO**: Add production deployment instructions for:
- Vercel/Netlify (frontend)
- Railway/Render/Fly.io (backend)
- AWS/GCP/Azure (full stack)

## Verification

### Backend Health Check

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "DocMemory API"
}
```

### Frontend Build Test

```bash
cd frontend
npm run build
```

### Run Tests

**Backend Tests:**
```bash
pytest tests/ -v
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port
# Windows:
netstat -ano | findstr :8000
# macOS/Linux:
lsof -i :8000

# Kill process or use different port
```

#### 2. Python Dependencies Installation Fails

**Error**: `ERROR: Could not build wheels for faiss-cpu`

**Solution**:
```bash
# Install system dependencies first
# Ubuntu/Debian:
sudo apt-get install build-essential python3-dev

# macOS:
xcode-select --install
brew install cmake

# Then retry pip install
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Node Modules Installation Fails

**Error**: `npm ERR! code ELIFECYCLE`

**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 4. FAISS Import Error

**Error**: `ModuleNotFoundError: No module named 'faiss'`

**Solution**:
```bash
# Install faiss-cpu explicitly
pip install faiss-cpu

# Or for GPU support (if available):
pip install faiss-gpu
```

#### 5. CORS Errors in Frontend

**Error**: `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**:
- Check `backend/core/config.py` CORS_ORIGINS setting
- Ensure frontend URL is included in allowed origins
- Restart backend server after configuration changes

## Development Tools

### Recommended IDE Extensions

**VS Code:**
- Python
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- Docker

### Useful Commands

**Backend:**
```bash
# Run with auto-reload
uvicorn backend.main:app --reload

# Run tests with coverage
pytest tests/ --cov=backend --cov=src

# Format code
black backend/ src/
```

**Frontend:**
```bash
# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint
```

## Next Steps

After setup:

1. **Read Documentation**:
   - [Architecture](./architecture.md)
   - [API Documentation](./api.md)
   - [Runbook](./runbook.md)

2. **Explore Codebase**:
   - Start with `main.py` for backend entry point
   - Check `frontend/app/page.tsx` for frontend entry
   - Review `src/` for core functionality

3. **Run Example**:
   ```bash
   python main.py
   ```

4. **Upload Test Document**:
   - Use the web interface at http://localhost:3000
   - Or use the API directly

## Getting Help

- **Documentation**: Check `/docs` folder
- **Issues**: GitHub Issues (TODO: Add link)
- **Discussions**: GitHub Discussions (TODO: Add link)

## TODO: Additional Setup Tasks

- [ ] Configure production environment variables
- [ ] Set up database migrations (when migrating to PostgreSQL)
- [ ] Configure Redis for caching
- [ ] Set up monitoring and logging
- [ ] Configure CI/CD secrets
- [ ] Set up SSL/TLS certificates
- [ ] Configure backup strategy

