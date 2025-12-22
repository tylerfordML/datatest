import sys
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Ensure project root is in sys.path for module resolution
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

@pytest.fixture(scope="session")
def client():
    """
    A Pytest fixture that provides a TestClient instance for FastAPI endpoints being used for Roman Num Service.

    Scope:
        session — the same client instance is reused across all tests in the session, improving test performance.

    Usage:
        def test_example(client):
            response = client.get("/health")
            assert response.status_code == 200

    Benefits:
    - Allows testing of HTTP endpoints without running a live server
    - Supports dependency injection and middleware exactly as in production
    
    """
    
    return TestClient(app)
