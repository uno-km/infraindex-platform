import pytest
import httpx
from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the InfraIndex API"}

@pytest.mark.asyncio
async def test_search_gpus_rate_limit():
    """Test that the search endpoint is reachable (200 or 429)"""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/search/gpus?q=H100")
        assert response.status_code in [200, 429]

@pytest.mark.asyncio
async def test_health_check():
    """Test the dependency-aware health check"""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/health")
        assert response.status_code in [200, 503]
        data = response.json()
        assert "status" in data
        assert "dependencies" in data
