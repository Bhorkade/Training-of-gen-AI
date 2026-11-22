import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure BASE_DIR is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Set test environment
os.environ["GEMINI_API_KEY"] = "fake-test-api-key"

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)
