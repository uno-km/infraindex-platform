import pytest
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_search_api_basic():
    response = client.post(
        "/api/v1/search/",
        json={"sort_by": "price_asc"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total" in data
    assert data["total"] == 0 # Mock implementation returns 0 currently
