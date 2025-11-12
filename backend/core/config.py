# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

"""
Application configuration
"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "DocMemory API"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    
    # TODO: Add production CORS origins
    
    # Storage
    STORAGE_PATH: str = "./docmemory_storage/"
    
    # TODO: Add database URL when migrating to PostgreSQL
    # DATABASE_URL: str = "postgresql://user:pass@localhost/dbname"
    
    # TODO: Add Redis URL for caching
    # REDIS_URL: str = "redis://localhost:6379"
    
    # TODO: Add authentication settings
    # SECRET_KEY: str
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

