import pytest
from fastapi.testclient import TestClient

from app.principal import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
