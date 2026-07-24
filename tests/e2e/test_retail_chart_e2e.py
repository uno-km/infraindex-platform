"""
tests/e2e/test_retail_chart_e2e.py
Phase 1 - 소매 차트 E2E 테스트
TestClient 진입 후 FastAPICache 재초기화 (lifespan startup이 Redis init을 덮어쓰기 때문)
"""
import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


class TestRetailChartE2E:

    @pytest.fixture
    def app_client(self):
        from fastapi.testclient import TestClient
        from apps.api.main import app
        from apps.api.core.database import get_db

        async def override_get_db():
            yield None

        app.dependency_overrides[get_db] = override_get_db

        with TestClient(app, raise_server_exceptions=False) as client:
            # lifespan startup 후 InMemoryBackend로 재초기화 (Redis 없음)
            FastAPICache.init(InMemoryBackend(), prefix="e2e-test")
            yield client

        app.dependency_overrides.clear()

    def test_unified_price_series_returns_200(self, app_client):
        """GET /api/v1/chart/unified-price-series 가 200을 반환해야 한다"""
        response = app_client.get(
            "/api/v1/chart/unified-price-series",
            params={"hw_typ": "gpu", "model_id": "H100"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_unified_price_series_empty_with_no_db(self, app_client):
        """DB 없을 때 빈 리스트를 반환해야 한다"""
        response = app_client.get(
            "/api/v1/chart/unified-price-series",
            params={"hw_typ": "gpu", "model_id": "H100"}
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_reports_daily_brief_accessible(self, app_client):
        """GET /api/v1/reports/daily-brief 가 200을 반환해야 한다"""
        response = app_client.get("/api/v1/reports/daily-brief")
        assert response.status_code == 200
        data = response.json()
        assert "date" in data
        assert "news" in data

    def test_invalid_hw_typ_returns_empty(self, app_client):
        """잘못된 hw_typ으로 요청 시 빈 리스트를 반환해야 한다"""
        response = app_client.get(
            "/api/v1/chart/unified-price-series",
            params={"hw_typ": "invalid", "model_id": "test"}
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_news_list_accessible(self, app_client):
        """GET /api/v1/news/ 가 200을 반환해야 한다"""
        response = app_client.get("/api/v1/news/")
        assert response.status_code == 200

    def test_papers_list_accessible(self, app_client):
        """GET /api/v1/papers/ 가 200을 반환해야 한다"""
        response = app_client.get("/api/v1/papers/")
        assert response.status_code == 200
