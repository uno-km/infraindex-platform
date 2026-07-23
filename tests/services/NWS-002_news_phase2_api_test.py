import pytest
from httpx import AsyncClient, ASGITransport
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch, MagicMock

def mock_rate_limiter(*args, **kwargs):
    for arg in args:
        if hasattr(arg, "state"):
            arg.state.view_rate_limit = []
            break


class TestNewsAPIPhase2:
    @pytest.mark.asyncio
    async def test_get_news_list(self):
        """뉴스 리스트 정상 조회 확인"""
        from apps.api.main import app
        from apps.api.core.database import get_db

        mock_db = AsyncMock()
        mock_result = MagicMock()
        
        # scalars().all() mock
        mock_article = AsyncMock()
        mock_article.id = uuid.uuid4()
        mock_article.title = "Test Phase 2 Article"
        mock_article.url = "http://test.com"
        mock_article.source_name = "TechCrunch"
        mock_article.published_at = datetime.now(timezone.utc)
        mock_article.summary = "Summary"
        mock_article.content_type = "article"

        mock_result.scalars.return_value.all.return_value = [mock_article]
        mock_db.execute.return_value = mock_result

        async def override_db():
            yield mock_db

        app.dependency_overrides[get_db] = override_db

        with patch("slowapi.extension.Limiter._check_request_limit", side_effect=mock_rate_limiter):
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://localhost") as ac:
                response = await ac.get("/api/v1/news")
                
        app.dependency_overrides.clear()

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "Test Phase 2 Article"
        assert data["items"][0]["source_name"] == "TechCrunch"

    @pytest.mark.asyncio
    async def test_get_news_sources(self):
        """소스 목록 조회 확인"""
        from apps.api.main import app
        from apps.api.core.database import get_db

        mock_db = AsyncMock()
        mock_result = MagicMock()
        
        mock_source = AsyncMock()
        mock_source.id = uuid.uuid4()
        mock_source.name = "Bloomberg"
        mock_source.country = "US"

        mock_result.scalars.return_value.all.return_value = [mock_source]
        mock_db.execute.return_value = mock_result

        async def override_db():
            yield mock_db

        app.dependency_overrides[get_db] = override_db

        with patch("slowapi.extension.Limiter._check_request_limit", side_effect=mock_rate_limiter):
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://localhost") as ac:
                response = await ac.get("/api/v1/news/sources")
                
        app.dependency_overrides.clear()

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Bloomberg"

    @pytest.mark.asyncio
    async def test_get_news_tags(self):
        """태그 목록 조회 확인"""
        from apps.api.main import app
        from apps.api.core.database import get_db

        mock_db = AsyncMock()
        mock_result = MagicMock()
        
        mock_tag = AsyncMock()
        mock_tag.id = uuid.uuid4()
        mock_tag.name = "AI"
        mock_tag.category = "Tech"

        mock_result.scalars.return_value.all.return_value = [mock_tag]
        mock_db.execute.return_value = mock_result

        async def override_db():
            yield mock_db

        app.dependency_overrides[get_db] = override_db

        with patch("slowapi.extension.Limiter._check_request_limit", side_effect=mock_rate_limiter):
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://localhost") as ac:
                response = await ac.get("/api/v1/news/tags")
                
        app.dependency_overrides.clear()

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "AI"
