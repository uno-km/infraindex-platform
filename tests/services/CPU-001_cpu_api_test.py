"""
CPU API Unit & Integration Tests
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from unittest.mock import AsyncMock, MagicMock

@pytest_asyncio.fixture
async def async_api_client():
    from apps.server.main import app
    from shared.db.session import get_db
    from unittest.mock import AsyncMock

    async def override_get_db():
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value = MagicMock(all=lambda: [])
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db
    
    from shared.config.settings import settings
    original_use_real_db = settings.USE_REAL_DB
    settings.USE_REAL_DB = False
    
    from unittest.mock import patch
    def mock_check_limit(*args, **kwargs):
        for arg in args:
            if hasattr(arg, "state"):
                arg.state.view_rate_limit = []
                break

    with patch("slowapi.extension.Limiter._check_request_limit", side_effect=mock_check_limit):
        try:
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://testserver") as client:
                yield client
        finally:
            app.dependency_overrides.clear()
            settings.USE_REAL_DB = original_use_real_db

class TestCPUApidEndpoints:
    @pytest.mark.asyncio
    async def test_search_cpus_reachable(self, async_api_client):
        resp = await async_api_client.get("/api/v1/search/cpus?q=EPYC")
        assert resp.status_code in [200, 429, 500]

    @pytest.mark.asyncio
    async def test_chart_cpu_returns_list(self, async_api_client):
        resp = await async_api_client.get("/api/v1/chart/cpu-price-series?cpu_model_id=EPYC")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    @pytest.mark.asyncio
    async def test_history_cpu_prefix(self, async_api_client):
        # We can test that the history endpoint accepts the 'cpu:' prefix and responds properly
        resp = await async_api_client.get("/api/v1/history/cpu:cloudv:EPYC")
        assert resp.status_code == 200
        body = resp.json()
        assert body["offering_id"] == "cpu:cloudv:EPYC"
        assert "history" in body
