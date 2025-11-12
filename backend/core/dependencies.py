# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

"""
Shared dependencies for FastAPI routes
"""
from functools import lru_cache
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import DocMemorySystem from main.py
from main import DocMemorySystem
from backend.core.config import settings

@lru_cache()
def get_docmemory_system():
    """
    Get or create DocMemory system instance
    Uses LRU cache to ensure singleton pattern
    """
    # TODO: Consider using dependency injection container
    return DocMemorySystem(storage_path=settings.STORAGE_PATH)

