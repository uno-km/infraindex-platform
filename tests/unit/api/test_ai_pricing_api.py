import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from apps.server.main import app
from shared.db.session import get_db

async def override_get_db():
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.all.return_value = [] # Return empty list for simplicity
    mock_db.execute.return_value = mock_result
    yield mock_db

app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_get_ai_pricing_latest():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
        response = await ac.get("/api/v1/ai-pricing/latest")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

@pytest.mark.asyncio
async def test_get_ai_pricing_history():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
        response = await ac.get("/api/v1/ai-pricing/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
