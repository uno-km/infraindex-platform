import pytest
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
from sqlalchemy import select
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.core.database import get_db
from apps.services.news.models import NewsDailyBriefing

client = TestClient(app)

@pytest.fixture
def mock_db():
    db = AsyncMock()
    # For session lifecycle (async with)
    db.__aenter__.return_value = db
    db.__aexit__.return_value = None
    return db

@pytest.mark.asyncio
async def test_llm_briefing_generation():
    """
    Test generating a briefing through ai_service
    """
    from apps.api.core.ai_service import generate_daily_news_briefing
    
    articles = [
        {"title": "Test 1", "source": "Source 1", "summary": "Summary 1", "category": "GPU"},
        {"title": "Test 2", "source": "Source 2", "summary": "Summary 2", "category": "AI"}
    ]
    
    # We don't want to actually call Ollama in unit tests, so we mock the OpenAI client inside ai_service
    with patch('apps.api.core.ai_service.client') as mock_client:
        mock_response = AsyncMock()
        mock_response.choices = [
            AsyncMock(message=AsyncMock(content="# AI Briefing\nThis is a test briefing."))
        ]
        # mock_client.chat.completions.create is a coroutine
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        
        result = await generate_daily_news_briefing("2026-07-23", articles)
        
        assert "This is a test briefing." in result
        mock_client.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_api_generate_briefing():
    """
    Test POST /api/v1/news/briefing/generate
    """
    # Overriding dependency
    async def override_get_db():
        from unittest.mock import MagicMock
        mock_db = AsyncMock()
        # Mock article selection
        mock_article_result = MagicMock()
        mock_article_result.scalars.return_value.all.return_value = [
            MagicMock(title="T1", summary="S1", category="GPU", source_name="src1", id=uuid.uuid4())
        ]
        # First execute is for articles, second is for checking existing briefing
        mock_briefing_result = MagicMock()
        mock_briefing_result.scalar_one_or_none.return_value = None
        
        mock_db.execute.side_effect = [mock_article_result, mock_briefing_result]
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db
    
    with patch('apps.api.core.ai_service.client') as mock_client:
        mock_response = AsyncMock()
        mock_response.choices = [
            AsyncMock(message=AsyncMock(content="# AI Briefing Mock"))
        ]
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        response = client.post("/api/v1/news/briefing/generate?date=2026-07-23", headers={"Host": "localhost"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["status"] == "success"
        assert "# AI Briefing Mock" in data["briefing"]
        
    app.dependency_overrides.clear()

