# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

"""
Shared dependencies for FastAPI routes
"""
from functools import lru_cache
from ..src.system import AethersiteSystem
from .config import settings

@lru_cache()
def get_docmemory_system():
    """
    Get or create Aethersite system instance
    Uses LRU cache to ensure singleton pattern
    """
    # TODO: Consider using dependency injection container
    return AethersiteSystem(storage_path=settings.STORAGE_PATH)
