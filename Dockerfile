# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

# Multi-stage build for DocMemory
FROM python:3.9-slim as backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY requirements.txt backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r backend/requirements.txt

# Copy backend code
COPY src/ ./src/
COPY backend/ ./backend/
COPY main.py ./

# TODO: Add production optimizations
# TODO: Add healthcheck
# TODO: Configure non-root user

FROM node:20-alpine as frontend

WORKDIR /app

# Copy frontend files
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ ./
RUN npm run build

# Production stage
FROM python:3.9-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from backend stage
COPY --from=backend /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=backend /usr/local/bin /usr/local/bin

# Copy backend code
COPY --from=backend /app/src ./src
COPY --from=backend /app/backend ./backend
COPY --from=backend /app/main.py ./

# Copy frontend build
COPY --from=frontend /app/.next ./frontend/.next
COPY --from=frontend /app/public ./frontend/public

# TODO: Add environment variables
ENV PYTHONUNBUFFERED=1
ENV STORAGE_PATH=/app/storage

# Expose ports
EXPOSE 8000

# Run backend API (frontend can be served separately or via nginx)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

