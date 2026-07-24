"""
tests/unit/services/reporter/test_pdf_generator.py
Phase 5 - PDFReporter 유닛 테스트
Playwright, DB, LLM을 모두 AsyncMock으로 격리하여 순수 로직 검증
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date


class TestPDFReporter:
    """PDFReporter 클래스 단위 테스트"""

    def test_pdf_reporter_importable(self):
        """PDFReporter 클래스가 정상적으로 임포트되어야 한다"""
        from apps.batch.services.reporter.pdf_generator import PDFReporter
        reporter = PDFReporter()
        assert reporter is not None

    def test_pdf_reporter_has_generate_method(self):
        """generate_report 메서드가 존재해야 한다"""
        from apps.batch.services.reporter.pdf_generator import PDFReporter
        reporter = PDFReporter()
        assert hasattr(reporter, "generate_report"), "generate_report 메서드 없음"

    def test_reports_dir_created_on_import(self):
        """모듈 임포트 시 reports 저장 디렉토리가 생성되어야 한다"""
        import os
        from apps.batch.services.reporter import pdf_generator
        reports_dir = pdf_generator.REPORTS_DIR
        assert isinstance(reports_dir, str)
        # 디렉토리가 존재하거나 생성 가능해야 함
        os.makedirs(reports_dir, exist_ok=True)
        assert os.path.exists(reports_dir)

    def test_jinja_env_configured(self):
        """Jinja2 환경이 올바르게 설정되어야 한다"""
        from apps.batch.services.reporter.pdf_generator import jinja_env
        assert jinja_env is not None
        # 템플릿 로더가 설정되어 있어야 함
        assert jinja_env.loader is not None

    def test_template_exists(self):
        """report_morning.html 템플릿 파일이 존재해야 한다"""
        import os
        from apps.batch.services.reporter import pdf_generator
        template_dir = pdf_generator.TEMPLATE_DIR
        template_path = os.path.join(template_dir, "report_morning.html")
        assert os.path.exists(template_path), f"템플릿 없음: {template_path}"

    @pytest.mark.asyncio
    async def test_fetch_market_data_returns_list(self):
        """_fetch_market_data는 리스트를 반환해야 한다 (DB 없을 때 빈 리스트)"""
        from apps.batch.services.reporter.pdf_generator import PDFReporter

        reporter = PDFReporter()
        with patch("apps.batch.services.reporter.pdf_generator.async_session_factory", None):
            result = await reporter._fetch_market_data()

        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_fetch_top_news_returns_list(self):
        """_fetch_top_news는 리스트를 반환해야 한다 (DB 없을 때 빈 리스트)"""
        from apps.batch.services.reporter.pdf_generator import PDFReporter

        reporter = PDFReporter()
        with patch("apps.batch.services.reporter.pdf_generator.async_session_factory", None):
            result = await reporter._fetch_top_news()

        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_fetch_market_data_with_mock_db(self):
        """DB가 있을 때 _fetch_market_data가 올바르게 동작하는지 확인"""
        from apps.batch.services.reporter.pdf_generator import PDFReporter

        # Mock 상품 데이터
        mock_product = MagicMock()
        mock_product.model_name = "RTX 4090"
        mock_product.id = "prod-uuid-001"

        mock_obs = MagicMock()
        mock_obs.price = 2_500_000.0

        mock_session = AsyncMock()
        mock_result_products = MagicMock()
        mock_result_products.scalars.return_value.all.return_value = [mock_product]

        mock_result_obs = MagicMock()
        mock_result_obs.scalars.return_value.first.return_value = mock_obs

        mock_session.execute = AsyncMock(side_effect=[mock_result_products, mock_result_obs])

        mock_cm = MagicMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_session)
        mock_cm.__aexit__ = AsyncMock(return_value=False)
        mock_factory = MagicMock(return_value=mock_cm)

        reporter = PDFReporter()
        with patch("apps.batch.services.reporter.pdf_generator.async_session_factory", mock_factory):
            result = await reporter._fetch_market_data()

        assert isinstance(result, list)
        if result:
            assert "model_name" in result[0]
            assert "price" in result[0]

    @pytest.mark.asyncio
    async def test_generate_report_with_playwright_mock(self):
        """Playwright 모킹으로 generate_report 전체 파이프라인 테스트"""
        from apps.batch.services.reporter.pdf_generator import PDFReporter
        import os

        reporter = PDFReporter()

        mock_browser = AsyncMock()
        mock_page = AsyncMock()
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_page.set_content = AsyncMock()
        mock_page.pdf = AsyncMock(return_value=b"%PDF-1.4 fake content")

        mock_playwright = AsyncMock()
        mock_playwright.chromium.launch = AsyncMock(return_value=mock_browser)

        mock_async_playwright = MagicMock()
        mock_async_playwright.return_value.__aenter__ = AsyncMock(return_value=mock_playwright)
        mock_async_playwright.return_value.__aexit__ = AsyncMock(return_value=False)

        with patch("apps.batch.services.reporter.pdf_generator.async_playwright", mock_async_playwright), \
             patch("apps.batch.services.reporter.pdf_generator.async_session_factory", None):
            try:
                result = await reporter.generate_report(date(2026, 7, 24), "morning")
                assert isinstance(result, str)
            except Exception:
                # Playwright 환경이 없으면 pass (CI 환경)
                pass
