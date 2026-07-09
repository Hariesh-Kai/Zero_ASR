import os
import sys

from fastapi.testclient import TestClient

# Add backend directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

client = TestClient(app)