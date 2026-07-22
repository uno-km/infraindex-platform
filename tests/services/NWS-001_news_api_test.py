import pytest
from httpx import AsyncClient, ASGITransport
from apps.api.main import app
from apps.api.core.database import get_db
from datetime import datetime, timezone
import json

@pytest.mark.asyncio
async def test_news_api_structure(monkeypatch):
    from unittest.mock import AsyncMock, MagicMock

    mock_db = AsyncMock()
    mock_result = MagicMock()
    
    # id, title, url, source, published_at, summary, keywords
    mock_result.all.return_value = [
        MagicMock(
            id="1234",
            title="Nvidia announces new GPU",
            url="http://example.com/nvidia",
            source="Bloomberg",
            published_at=datetime.now(timezone.utc),
            summary="New GPU is fast.",
            keywords="Nvidia,GPU"
        ),
        MagicMock(
            id="5678",
            title="DRAM prices falling",
            url="http://example.com/dram",
            source="Naver",
            published_at=datetime.now(timezone.utc),
            summary="Memory is cheap.",
            keywords="DRAM,Samsung"
        )
    ]
    mock_db.execute.return_value = mock_result

    app.dependency_overrides[get_db] = lambda: mock_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/news?limit=10")
        
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["source"] == "Bloomberg"
    assert data[1]["source"] == "Naver"
    assert data[0]["keywords"] == "Nvidia,GPU"

    app.dependency_overrides.clear()
