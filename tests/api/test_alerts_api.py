import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from apps.api.main import app
from apps.api.core.database import get_db

async def override_get_db():
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result
    
    async def mock_refresh(instance):
        pass
    mock_db.refresh = AsyncMock(side_effect=mock_refresh)
    
    def mock_add(instance):
        from uuid import uuid4
        instance.id = uuid4()
    mock_db.add = MagicMock(side_effect=mock_add)
    
    yield mock_db

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:
        yield client

@pytest.mark.asyncio
async def test_get_alert_rules(async_client: AsyncClient):
    response = await async_client.get("/api/v1/alerts/rules")
    print("DEBUG RESPONSE:", response.text)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_create_alert_rule(async_client: AsyncClient):
    payload = {
        "target": "RTX 4080",
        "alert_type": "retail_price",
        "price_threshold": 1500000.0,
        "is_active": True
    }
    response = await async_client.post("/api/v1/alerts/rules", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["target"] == "RTX 4080"
    assert data["alert_type"] == "retail_price"
    assert data["price_threshold"] == 1500000.0

@pytest.mark.asyncio
async def test_get_alert_history(async_client: AsyncClient):
    response = await async_client.get("/api/v1/alerts/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_mark_alert_read(async_client: AsyncClient):
    # First, let's create a rule and an alert history manually or we can mock it.
    # We will test the endpoint returns 404 for non-existent.
    response = await async_client.post(f"/api/v1/alerts/history/{uuid4()}/read")
    assert response.status_code == 404
