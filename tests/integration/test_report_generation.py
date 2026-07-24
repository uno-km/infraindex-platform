"""
tests/integration/test_report_generation.py
Phase 5 - 리포트 생성 파이프라인 통합 테스트
reports.py API → _fetch_price_data → Excel/Word 생성 전체 플로우 검증
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone, date
import io


class TestReportGenerationPipeline:
    """리포트 생성 파이프라인 통합 테스트"""

    @pytest.mark.asyncio
    async def test_fetch_price_data_attribute_names_correct(self):
        """
        Bug Fix 검증: _fetch_price_data가 r.prv_id, r.gpu_mdl을 올바르게 참조하는지 테스트
        (이전 r.provider_id, r.gpu_model AttributeError 수정 확인)
        """
        from apps.api.api.v1.endpoints.reports import _fetch_price_data

        # 실제 Row 객체처럼 prv_id, gpu_mdl 속성을 가진 mock
        mock_row = MagicMock()
        mock_row.day = date(2026, 7, 22)
        mock_row.prv_id = "aws"
        mock_row.gpu_mdl = "H100"
        mock_row.min_price = 2.50
        mock_row.avg_price = 2.75
        mock_row.max_price = 3.00
        mock_row.cnt = 10

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.all.return_value = [mock_row]
        mock_db.execute = AsyncMock(return_value=mock_result)

        # AttributeError 없이 실행되어야 함
        result = await _fetch_price_data(mock_db, "H100", days=7)

        assert len(result) == 1
        assert result[0]["provider"] == "aws"
        assert result[0]["gpu_model"] == "H100"
        assert result[0]["min_price"] == 2.50
        assert result[0]["avg_price"] == 2.75

    @pytest.mark.asyncio
    async def test_excel_export_pipeline_no_data(self):
        """데이터 없을 때 Excel 파일이 빈 데이터와 함께 생성되어야 한다"""
        from apps.api.api.v1.endpoints.reports import export_excel

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)

        response = await export_excel(gpu_model_id="H100", days=30, db=mock_db)

        # StreamingResponse 반환 확인
        assert response is not None
        assert "excel" in response.media_type or "spreadsheet" in response.media_type

    @pytest.mark.asyncio
    async def test_excel_export_pipeline_with_data(self):
        """데이터가 있을 때 Excel 파일이 정상 생성되어야 한다"""
        from apps.api.api.v1.endpoints.reports import export_excel

        mock_row = MagicMock()
        mock_row.day = date(2026, 7, 22)
        mock_row.prv_id = "aws"
        mock_row.gpu_mdl = "H100"
        mock_row.min_price = 2.50
        mock_row.avg_price = 2.75
        mock_row.max_price = 3.00
        mock_row.cnt = 5

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.all.return_value = [mock_row]
        mock_db.execute = AsyncMock(return_value=mock_result)

        response = await export_excel(gpu_model_id="H100", days=30, db=mock_db)

        assert response is not None
        assert "H100" in response.headers.get("content-disposition", "")

    @pytest.mark.asyncio
    async def test_daily_brief_json_structure(self):
        """GET /daily-brief가 올바른 JSON 구조를 반환해야 한다"""
        from apps.api.api.v1.endpoints.reports import get_daily_brief_json

        result = await get_daily_brief_json()

        assert "date" in result
        assert "news" in result
        assert "power" in result
        assert "memory" in result

        assert isinstance(result["news"], list)
        assert isinstance(result["power"], list)
        assert isinstance(result["memory"], list)

        # 각 항목 구조 확인
        if result["news"]:
            assert "title" in result["news"][0]
            assert "source" in result["news"][0]

        if result["power"]:
            assert "region" in result["power"][0]
            assert "cost_per_kwh_usd" in result["power"][0]

        if result["memory"]:
            assert "component" in result["memory"][0]
            assert "price_usd" in result["memory"][0]
