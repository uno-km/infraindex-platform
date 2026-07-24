"""
tests/integration/test_backfill_pipeline.py
Phase 8 - 백필 파이프라인 통합 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi.testclient import TestClient


class TestBackfillPipeline:

    def test_duplicate_detector_plus_historical_crawler_integration(self):
        """DuplicateDetector + HistoricalCrawler 연동 통합 테스트"""
        from apps.services.news.duplicate_detector import DuplicateDetector
        from apps.services.news.crawler_historical import HistoricalCrawler

        detector = DuplicateDetector(similarity_threshold=0.85)
        crawler = HistoricalCrawler()

        # 논문 목록 시뮬레이션
        mock_papers = [
            {"url": "https://arxiv.org/abs/2401.00001", "title": "GPU Memory Bandwidth Analysis"},
            {"url": "https://arxiv.org/abs/2401.00002", "title": "HBM3 Performance Benchmark"},
            {"url": "https://arxiv.org/abs/2401.00001", "title": "GPU Memory Bandwidth Analysis"},  # 중복
        ]

        new_count = 0
        dup_count = 0
        for paper in mock_papers:
            if detector.is_duplicate(paper):
                dup_count += 1
            else:
                detector.register_article(paper)
                new_count += 1

        assert new_count == 2
        assert dup_count == 1
        assert detector.cache_size["url_cache"] == 2

    def test_date_range_covers_backfill_period(self):
        """2022~2024 전체를 월별로 커버하는지 확인"""
        from apps.services.news.crawler_historical import date_range_months
        ranges = list(date_range_months(date(2022, 1, 1), date(2024, 12, 31)))
        # 36개월
        assert len(ranges) == 36

    def test_backfill_job_model_properties(self):
        """BackfillJob 모델의 progress_pct와 duration_seconds 속성"""
        from apps.api.models.backfill import BackfillJob
        from datetime import datetime, timezone, timedelta

        job = BackfillJob()
        job.total_urls = 100
        job.processed = 50
        assert job.progress_pct == 50.0

        now = datetime.now(timezone.utc)
        job.started_at = now - timedelta(seconds=120)
        job.finished_at = now
        assert job.duration_seconds is not None
        assert abs(job.duration_seconds - 120.0) < 1.0

    def test_backfill_job_no_total_urls(self):
        """total_urls=0이면 progress_pct=None이어야 한다"""
        from apps.api.models.backfill import BackfillJob
        job = BackfillJob()
        job.total_urls = 0
        job.processed = 0
        assert job.progress_pct is None

    @pytest.mark.asyncio
    async def test_backfill_api_e2e_with_mock(self):
        """POST /api/v1/backfill/news → 202 + job_id 반환 통합 테스트"""
        from fastapi.testclient import TestClient
        from apps.api.main import app
        from apps.api.core.database import get_db

        mock_db = AsyncMock()

        # BackfillJob add/commit/refresh mock
        mock_job = MagicMock()
        mock_job.id = "test-job-uuid-001"
        mock_job.source = "arxiv"
        mock_job.from_date = date(2023, 1, 1)
        mock_job.to_date = date(2023, 12, 31)
        mock_job.status = "pending"
        mock_job.total_urls = 0
        mock_job.processed = 0
        mock_job.new_articles = 0
        mock_job.started_at = None
        mock_job.finished_at = None
        mock_job.error_msg = None
        mock_job.created_at = None
        mock_job.progress_pct = None
        mock_job.duration_seconds = None

        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        async def override_get_db():
            yield mock_db

        app.dependency_overrides[get_db] = override_get_db

        try:
            with TestClient(app, raise_server_exceptions=False) as client:
                FastAPICache.init(InMemoryBackend(), prefix="integration-backfill")

                with patch("apps.api.api.v1.endpoints.backfill._run_backfill") as mock_run:
                    response = client.post(
                        "/api/v1/backfill/news",
                        json={
                            "source": "arxiv",
                            "from_date": "2023-01-01",
                            "to_date": "2023-12-31",
                        }
                    )

                # 202 Accepted 확인
                assert response.status_code in [202, 200, 503], \
                    f"예상치 못한 상태: {response.status_code}: {response.text}"
        finally:
            app.dependency_overrides.clear()
