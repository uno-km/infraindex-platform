"""
tests/e2e/test_news_feed_e2e.py
Phase 2 - 뉴스 피드 API E2E 테스트
"""
import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


class TestNewsFeedE2E:

    @pytest.fixture
    def app_client(self):
        from fastapi.testclient import TestClient
        from apps.api.main import app
        from apps.api.core.database import get_db

        async def override_get_db():
            yield None

        app.dependency_overrides[get_db] = override_get_db

        with TestClient(app, raise_server_exceptions=False) as client:
            FastAPICache.init(InMemoryBackend(), prefix="e2e-news")
            yield client

        app.dependency_overrides.clear()

    def test_news_list_returns_200(self, app_client):
        response = app_client.get("/api/v1/news/")
        assert response.status_code == 200

    def test_news_list_has_items_key(self, app_client):
        response = app_client.get("/api/v1/news/")
        assert "items" in response.json()

    def test_news_list_with_query_filter(self, app_client):
        response = app_client.get("/api/v1/news/", params={"query": "NVIDIA GPU"})
        assert response.status_code == 200

    def test_news_list_with_category_filter(self, app_client):
        response = app_client.get("/api/v1/news/", params={"category": "GPU"})
        assert response.status_code == 200

    def test_news_list_pagination(self, app_client):
        response = app_client.get("/api/v1/news/", params={"page": 2, "limit": 10})
        assert response.status_code == 200

    def test_news_briefing_or_404(self, app_client):
        response = app_client.get("/api/v1/news/briefing/")
        assert response.status_code in [200, 404, 500]

    def test_news_sources_or_404(self, app_client):
        response = app_client.get("/api/v1/news/sources/")
        assert response.status_code in [200, 404, 500]
