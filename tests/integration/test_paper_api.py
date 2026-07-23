import pytest
import asyncio
import os
from httpx import AsyncClient, ASGITransport

os.environ["USE_REAL_DB"] = "True"
from apps.api.main import app

@pytest.mark.asyncio
async def test_paper_api_integration():
    # Because we're using memory/local db, we can just test the endpoints
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Trigger crawl
        # Warning: This will actually call arxiv. We'll set max_results to 1
        response = await ac.post("/api/v1/papers/crawl/arxiv?max_results=2")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        # 2. List papers
        response = await ac.get("/api/v1/papers/")
        assert response.status_code == 200
        list_data = response.json()
        assert list_data["total"] >= 0
        
        if list_data["total"] > 0:
            paper_id = list_data["items"][0]["id"]
            
            # 3. Get single paper
            response = await ac.get(f"/api/v1/papers/{paper_id}")
            assert response.status_code == 200
            single_data = response.json()
            assert single_data["id"] == paper_id
            assert "external_id" in single_data
