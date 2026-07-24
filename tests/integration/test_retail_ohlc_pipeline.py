"""
tests/integration/test_retail_ohlc_pipeline.py
Phase 1 - 소매 OHLC 파이프라인 통합 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone, date


class TestRetailOHLCPipeline:
    """소매 크롤러 -> OHLC 집계 -> DB 저장 파이프라인 통합 테스트"""

    def test_calculate_ohlc_integrates_with_apexcharts_format(self):
        """calculate_ohlc -> ohlc_to_apexcharts 체인이 올바른 형식을 반환해야 한다"""
        from apps.services.market.ohlc_aggregator import calculate_ohlc, ohlc_to_apexcharts

        prices = [
            (datetime(2026, 7, 1, 9, 0, tzinfo=timezone.utc), 2_200_000),
            (datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc), 2_500_000),
            (datetime(2026, 7, 1, 18, 0, tzinfo=timezone.utc), 2_100_000),
            (datetime(2026, 7, 1, 22, 0, tzinfo=timezone.utc), 2_350_000),
        ]

        ohlc = calculate_ohlc(prices)
        apex_row = ohlc_to_apexcharts({
            "trade_date": date(2026, 7, 1),
            "open_price": ohlc["open"],
            "high_price": ohlc["high"],
            "low_price": ohlc["low"],
            "close_price": ohlc["close"],
        })

        assert "x" in apex_row
        assert "o" in apex_row
        assert "h" in apex_row
        assert "l" in apex_row
        assert "c" in apex_row
        assert apex_row["h"] >= apex_row["l"]
        assert apex_row["o"] == ohlc["open"]
        assert apex_row["c"] == ohlc["close"]

    def test_compute_summary_integrates_with_ohlc(self):
        """compute_summary가 OHLC 데이터를 올바르게 요약해야 한다"""
        from apps.services.market.ohlc_aggregator import compute_summary

        ohlc_rows = [
            {"trade_date": date(2026, 7, 1), "close_price": 2_350_000,
             "high_price": 2_500_000, "low_price": 2_100_000},
            {"trade_date": date(2026, 7, 2), "close_price": 2_400_000,
             "high_price": 2_600_000, "low_price": 2_200_000},
        ]

        summary = compute_summary(ohlc_rows)

        # 실제 반환 키 확인
        assert "current_price" in summary
        assert "all_time_high" in summary
        assert "all_time_low" in summary
        # 값 검증
        assert summary["all_time_high"] == 2_600_000
        assert summary["all_time_low"] == 2_100_000
        assert summary["current_price"] == 2_400_000

    @pytest.mark.asyncio
    async def test_retail_crawler_triggers_alert_below_threshold(self):
        """가격이 임계값 이하로 내려가면 AlertEngine이 트리거되어야 한다"""
        from apps.services.alerts.alert_engine import AlertEngine

        mock_db = AsyncMock()
        mock_rule = MagicMock()
        mock_rule.id = "rule-uuid-001"
        mock_rule.alert_type = "retail_price"
        mock_rule.target = "RTX 4090"
        mock_rule.price_threshold = 2_000_000.0
        mock_rule.is_active = True

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_rule]
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()

        engine = AlertEngine()
        alerts = await engine.check_retail_alerts(
            db=mock_db,
            product_name="RTX 4090",
            new_price=1_900_000.0,
            link_url="https://shop.example.com/rtx4090"
        )

        assert len(alerts) == 1
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_retail_crawler_no_alert_above_threshold(self):
        """가격이 임계값 초과인 경우 알림이 트리거되지 않아야 한다"""
        from apps.services.alerts.alert_engine import AlertEngine

        mock_db = AsyncMock()
        mock_rule = MagicMock()
        mock_rule.alert_type = "retail_price"
        mock_rule.target = "RTX 4090"
        mock_rule.price_threshold = 2_000_000.0
        mock_rule.is_active = True

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_rule]
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()

        engine = AlertEngine()
        alerts = await engine.check_retail_alerts(
            db=mock_db,
            product_name="RTX 4090",
            new_price=2_500_000.0,
            link_url="https://shop.example.com/rtx4090"
        )

        assert len(alerts) == 0
        mock_db.add.assert_not_called()
