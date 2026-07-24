"""
tests/unit/services/market/test_ohlc_aggregator.py

Phase 1 — OHLC 집계 로직 단위 테스트
TDD Red 단계: 구현 전 먼저 작성
"""
import pytest
from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch


# ====================================================================
# 1. 순수 OHLC 계산 로직 테스트 (DB 의존성 없음)
# ====================================================================

class TestOHLCCalculation:
    """
    가격 포인트 리스트 → OHLC 4값 계산이 올바른지 검증
    """

    def test_basic_ohlc_calculation(self):
        """기본 OHLC 값 계산 정확도 검증"""
        from apps.batch.services.market.ohlc_aggregator import calculate_ohlc
        
        prices = [
            (datetime(2026, 7, 1, 9, 0), 2_200_000),   # 첫 관측 → open
            (datetime(2026, 7, 1, 12, 0), 2_500_000),  # 최고가 → high
            (datetime(2026, 7, 1, 15, 0), 2_100_000),  # 최저가 → low
            (datetime(2026, 7, 1, 21, 0), 2_350_000),  # 마지막 → close
        ]
        
        result = calculate_ohlc(prices)
        
        assert result["open"] == 2_200_000
        assert result["high"] == 2_500_000
        assert result["low"] == 2_100_000
        assert result["close"] == 2_350_000
        assert result["volume"] == 4

    def test_single_price_point_ohlc(self):
        """단일 가격 포인트에서 OHLC 모두 동일해야 함"""
        from apps.batch.services.market.ohlc_aggregator import calculate_ohlc
        
        prices = [(datetime(2026, 7, 1, 9, 0), 3_000_000)]
        result = calculate_ohlc(prices)
        
        assert result["open"] == 3_000_000
        assert result["high"] == 3_000_000
        assert result["low"] == 3_000_000
        assert result["close"] == 3_000_000

    def test_average_price_calculation(self):
        """평균가 계산 정확도 검증"""
        from apps.batch.services.market.ohlc_aggregator import calculate_ohlc
        
        prices = [
            (datetime(2026, 7, 1, 9, 0), 1000),
            (datetime(2026, 7, 1, 12, 0), 2000),
            (datetime(2026, 7, 1, 18, 0), 3000),
        ]
        result = calculate_ohlc(prices)
        
        assert result["avg"] == 2000.0

    def test_empty_prices_raises(self):
        """빈 가격 목록은 ValueError를 발생시켜야 함"""
        from apps.batch.services.market.ohlc_aggregator import calculate_ohlc
        
        with pytest.raises(ValueError, match="prices must not be empty"):
            calculate_ohlc([])

    def test_prices_sorted_by_time(self):
        """시간 정렬 없이 들어온 데이터도 올바르게 처리해야 함"""
        from apps.batch.services.market.ohlc_aggregator import calculate_ohlc
        
        # 시간 역순으로 입력
        prices = [
            (datetime(2026, 7, 1, 21, 0), 2_350_000),  # 마지막
            (datetime(2026, 7, 1, 9, 0), 2_200_000),   # 첫 번째
        ]
        result = calculate_ohlc(prices)
        
        # 정렬 후 처리되어야 함
        assert result["open"] == 2_200_000   # 시간순 첫번째
        assert result["close"] == 2_350_000  # 시간순 마지막


# ====================================================================
# 2. OHLCAggregator 클래스 메서드 테스트 (DB Mocking)
# ====================================================================

class TestOHLCAggregator:
    """
    DB 연동 집계 로직을 Mock을 통해 단위 테스트
    """

    @pytest.mark.asyncio
    async def test_aggregate_daily_with_data(self):
        """
        하루치 관측 데이터가 있을 때 OHLC 집계 후 DB upsert 호출 검증
        """
        from apps.batch.services.market.ohlc_aggregator import OHLCAggregator
        
        aggregator = OHLCAggregator()
        mock_db = AsyncMock()
        
        # DB에서 반환할 가격 관측 Mock 데이터
        mock_obs = [
            MagicMock(price=2_200_000, observed_at=datetime(2026, 7, 1, 9, 0, tzinfo=timezone.utc)),
            MagicMock(price=2_500_000, observed_at=datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)),
            MagicMock(price=2_100_000, observed_at=datetime(2026, 7, 1, 15, 0, tzinfo=timezone.utc)),
            MagicMock(price=2_350_000, observed_at=datetime(2026, 7, 1, 21, 0, tzinfo=timezone.utc)),
        ]
        
        mock_product_id = "test-product-uuid-1234"
        
        with patch.object(aggregator, '_fetch_observations', return_value=mock_obs):
            with patch.object(aggregator, '_upsert_ohlc', new_callable=AsyncMock) as mock_upsert:
                with patch.object(aggregator, '_fetch_product_ids', return_value=[mock_product_id]):
                    result = await aggregator.aggregate_daily(mock_db, date(2026, 7, 1))
        
        # upsert 가 한 번 호출되었는지
        assert mock_upsert.call_count == 1
        
        # upsert 인자가 올바른 OHLC 값인지
        call_args = mock_upsert.call_args[0]
        ohlc_data = call_args[1]  # 두 번째 인자가 OHLC dict
        
        assert ohlc_data["open_price"] == 2_200_000
        assert ohlc_data["high_price"] == 2_500_000
        assert ohlc_data["low_price"] == 2_100_000
        assert ohlc_data["close_price"] == 2_350_000

    @pytest.mark.asyncio
    async def test_aggregate_daily_no_data(self):
        """
        하루치 관측 데이터가 없을 때 upsert가 호출되지 않아야 함
        """
        from apps.batch.services.market.ohlc_aggregator import OHLCAggregator
        
        aggregator = OHLCAggregator()
        mock_db = AsyncMock()
        
        mock_product_id = "test-product-uuid-5678"
        
        with patch.object(aggregator, '_fetch_observations', return_value=[]):
            with patch.object(aggregator, '_upsert_ohlc', new_callable=AsyncMock) as mock_upsert:
                with patch.object(aggregator, '_fetch_product_ids', return_value=[mock_product_id]):
                    result = await aggregator.aggregate_daily(mock_db, date(2026, 7, 1))
        
        # 데이터가 없으면 upsert 미호출
        assert mock_upsert.call_count == 0

    def test_vendor_count_included(self):
        """여러 벤더의 가격이 포함될 때 vendor_count가 올바른지 검증"""
        from apps.batch.services.market.ohlc_aggregator import calculate_ohlc
        
        # 3개 판매처의 가격 (listing_vendor 정보 포함)
        prices = [
            (datetime(2026, 7, 1, 9, 0), 2_200_000),
            (datetime(2026, 7, 1, 10, 0), 2_300_000),
            (datetime(2026, 7, 1, 11, 0), 2_250_000),
        ]
        
        result = calculate_ohlc(prices)
        assert result["volume"] == 3


# ====================================================================
# 3. API 응답 형식 테스트 (ApexCharts 호환성)
# ====================================================================

class TestOHLCAPISchema:
    """
    API 응답이 ApexCharts OHLC candlestick 형식인지 검증
    { x: ISO date string, o: float, h: float, l: float, c: float }
    """

    def test_ohlc_to_apexcharts_format(self):
        """OHLC → ApexCharts 변환 포맷 검증"""
        from apps.batch.services.market.ohlc_aggregator import ohlc_to_apexcharts

        raw = {
            "trade_date": date(2026, 7, 1),
            "open_price": 2_200_000,
            "high_price": 2_500_000,
            "low_price": 2_100_000,
            "close_price": 2_350_000,
        }

        result = ohlc_to_apexcharts(raw)

        assert "x" in result
        assert "o" in result
        assert "h" in result
        assert "l" in result
        assert "c" in result
        assert result["o"] == 2_200_000
        assert result["h"] == 2_500_000
        assert result["l"] == 2_100_000
        assert result["c"] == 2_350_000
        assert isinstance(result["x"], str)  # ISO date string

    def test_summary_schema(self):
        """차트 요약 응답 스키마 검증"""
        from apps.batch.services.market.ohlc_aggregator import compute_summary

        ohlc_rows = [
            {"trade_date": date(2026, 7, 1), "open_price": 2_200_000, "high_price": 2_500_000, "low_price": 2_100_000, "close_price": 2_350_000},
            {"trade_date": date(2026, 7, 2), "open_price": 2_350_000, "high_price": 2_600_000, "low_price": 2_300_000, "close_price": 2_400_000},
        ]

        summary = compute_summary(ohlc_rows)

        assert "current_price" in summary
        assert "change_1d" in summary
        assert "change_pct_1d" in summary
        assert "all_time_high" in summary
        assert "all_time_low" in summary
        assert summary["all_time_high"] == 2_600_000
        assert summary["all_time_low"] == 2_100_000
        assert summary["current_price"] == 2_400_000  # 마지막 close
