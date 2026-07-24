"""
tests/unit/services/news/test_duplicate_detector.py
Phase 2 - 뉴스 중복 감지 로직 유닛 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestDuplicateDetection:
    """뉴스 기사 URL 중복 감지 로직 테스트"""

    def test_url_normalization_prevents_duplicates(self):
        """URL 정규화로 중복을 방지해야 한다"""
        urls = [
            "https://example.com/article",
            "https://example.com/article/",
            "http://example.com/article",
        ]
        normalized = set(u.rstrip("/").replace("http://", "https://") for u in urls)
        assert len(normalized) == 1

    def test_paper_service_importable(self):
        """PaperService가 정상적으로 임포트되어야 한다"""
        from apps.batch.services.paper.paper_service import PaperService
        assert PaperService is not None

    @pytest.mark.asyncio
    async def test_paper_service_upsert_skips_existing_paper(self):
        """
        PaperService: 이미 존재하는 external_id의 논문은 add하지 않고 update만 해야 한다
        """
        from apps.batch.services.paper.paper_service import PaperService
        from apps.batch.services.paper.crawler_arxiv import ArXivCrawler

        mock_db = AsyncMock()
        mock_source = MagicMock()
        mock_source.id = "src-uuid-001"
        mock_source.name = "arxiv"

        mock_existing = MagicMock()
        mock_existing.external_id = "arxiv:existing001"
        mock_existing.metadata_json = {}

        mock_source_result = MagicMock()
        mock_source_result.scalars.return_value.first.return_value = mock_source

        mock_paper_result = MagicMock()
        mock_paper_result.scalars.return_value.first.return_value = mock_existing

        mock_db.execute = AsyncMock(side_effect=[mock_source_result, mock_paper_result])
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()

        mock_papers = [{
            "external_id": "arxiv:existing001",
            "title": "Updated Title",
            "published_at": None,
            "category": "cs.AI",
            "metadata_json": {"abstract": "New abstract"}
        }]

        service = PaperService(mock_db)
        with patch.object(ArXivCrawler, "fetch_recent", new_callable=AsyncMock, return_value=mock_papers):
            count = await service.crawl_and_save_arxiv_recent(max_results=1)

        assert count == 0
        mock_db.add.assert_not_called()
        assert mock_existing.metadata_json == {"abstract": "New abstract"}

    def test_duplicate_url_pattern_string_comparison(self):
        """URL 중복 감지는 정규화된 문자열 비교여야 한다"""
        test_cases = [
            ("https://tc.com/article", "https://tc.com/article", True),
            ("https://ex.com/news", "https://ex.com/news/", True),
            ("https://ex.com/article-1", "https://ex.com/article-2", False),
        ]
        for url1, url2, expected in test_cases:
            is_duplicate = (url1.rstrip("/") == url2.rstrip("/"))
            assert is_duplicate == expected
