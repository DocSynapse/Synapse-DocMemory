# → Architecture & Build by DocSynapse
# Intelligent by Design. Crafted for Humanity.

"""
Pytest configuration and shared fixtures
"""
import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture(scope="session")
def temp_storage():
    """Create temporary storage directory for tests"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def cleanup_test_files():
    """Cleanup test files after each test"""
    yield
    # TODO: Implement cleanup logic
    pass

