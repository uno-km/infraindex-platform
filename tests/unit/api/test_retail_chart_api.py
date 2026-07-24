"""
tests/unit/api/test_retail_chart_api.py
Phase 1 - 소매 차트 API 유닛 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


@pytest.fixture(autouse=True)
def init_cache():
    """FastAPICache 초기화 (캐시 데코레이터가 붙은 엔드포인트 테스트 시 필요)"""
    FastAPICache.init(InMemoryBackend(), prefix="test")
    yield


class TestRetailChartAPI:
    """소매 차트 API 엔드포인트 유닛 테스트"""

    def test_chart_router_importable(self):
        """chart 라우터가 임포트 가능해야 한다"""
        from apps.server.api.v1.endpoints.chart import router
        assert router is not None

    def test_unified_price_series_route_exists(self):
        """/unified-price-series 라우트가 등록되어야 한다"""
        from apps.server.api.v1.endpoints.chart import router
        routes = [r.path for r in router.routes]
        assert any("unified-price-series" in r for r in routes), \
            f"unified-price-series 라우트 없음, 실제: {routes}"

    def test_candlestick_route_exists(self):
        """/candlestick 라우트가 등록되어야 한다"""
        from apps.server.api.v1.endpoints.chart import router
        routes = [r.path for r in router.routes]
        assert any("candlestick" in r for r in routes)

    def test_price_series_route_exists(self):
        """/price-series 라우트가 등록되어야 한다"""
        from apps.server.api.v1.endpoints.chart import router
        routes = [r.path for r in router.routes]
        assert any("price-series" in r for r in routes)

    def test_cpu_price_series_route_exists(self):
        """/cpu-price-series 라우트가 등록되어야 한다"""
        from apps.server.api.v1.endpoints.chart import router
        routes = [r.path for r in router.routes]
        assert any("cpu-price-series" in r for r in routes)

    @pytest.mark.asyncio
    async def test_unified_price_series_db_none_returns_empty(self):
        """DB가 None일 때 unified-price-series는 빈 리스트를 반환해야 한다"""
        from apps.server.api.v1.endpoints.chart import get_unified_price_series
        result = await get_unified_price_series(
            hw_typ="gpu",
            model_id="H100",
            provider=None,
            days=30,
            db=None
        )
        assert result == []

    @pytest.mark.asyncio
    async def test_unified_price_series_calls_db(self):
        """unified-price-series가 DB를 조회해야 한다"""
        from apps.server.api.v1.endpoints.chart import get_unified_price_series

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.all.return_value = []  # 빈 결과
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await get_unified_price_series(
            hw_typ="gpu",
            model_id="H100",
            provider=None,
            days=30,
            db=mock_db
        )

        # 빈 결과이면 빈 리스트 반환
        assert result == []
        mock_db.execute.assert_called_once()
