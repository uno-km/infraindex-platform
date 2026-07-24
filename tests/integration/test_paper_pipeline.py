"""
tests/integration/test_paper_pipeline.py
Phase 6 - ArXiv 크롤러 -> 파싱 -> DB 저장 파이프라인 통합 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date


class TestPaperPipeline:
    """ArXiv 크롤러 -> PaperService -> DB 저장 파이프라인 통합 테스트"""

    def test_arxiv_parser_output_compatible_with_paper_service(self):
        """
        ArXivCrawler._parse_entry 출력이 PaperService에서 요구하는 형식과 호환되어야 한다.
        feedparser entry의 links는 .href 속성이 있는 객체여야 함.
        """
        from apps.services.paper.crawler_arxiv import ArXivCrawler

        crawler = ArXivCrawler()

        # feedparser 실제 동작처럼 link를 MagicMock 객체로 (dict가 아닌 object)
        mock_pdf_link = MagicMock()
        mock_pdf_link.__getitem__ = lambda self, key: "pdf" if key == "title" else "https://arxiv.org/pdf/2507.12345"
        mock_pdf_link.get = lambda key, default=None: "pdf" if key == "title" else "https://arxiv.org/pdf/2507.12345"
        mock_pdf_link.href = "https://arxiv.org/pdf/2507.12345"

        # link.get('title') == 'pdf' 검사를 통과하도록 설정
        mock_pdf_link_dict = MagicMock()
        mock_pdf_link_dict.get.return_value = "pdf"
        mock_pdf_link_dict.href = "https://arxiv.org/pdf/2507.12345"

        author1 = MagicMock()
        author1.name = "John Smith"
        author2 = MagicMock()
        author2.name = "Jane Doe"

        mock_entry = MagicMock()
        mock_entry.id = "http://arxiv.org/abs/2507.12345v1"
        mock_entry.title = "Advances in GPU Architecture for AI Workloads"
        mock_entry.summary = "This paper presents novel GPU architecture improvements for AI."
        mock_entry.authors = [author1, author2]
        mock_entry.tags = [{"term": "cs.AI"}, {"term": "cs.LG"}]
        mock_entry.published = "2026-07-20T10:00:00Z"
        mock_entry.links = [mock_pdf_link_dict]
        mock_entry.link = "https://arxiv.org/abs/2507.12345"

        result = crawler._parse_entry(mock_entry)

        assert result is not None, "parse_entry가 None을 반환함"
        assert "external_id" in result
        assert result["external_id"].startswith("arxiv:")
        assert "title" in result
        assert "published_at" in result
        assert "category" in result
        assert "metadata_json" in result
        assert "authors" in result["metadata_json"]
        assert "abstract" in result["metadata_json"]

    @pytest.mark.asyncio
    async def test_paper_service_upsert_new_paper(self):
        """PaperService가 새 논문을 DB에 저장하는 통합 플로우 테스트"""
        from apps.services.paper.paper_service import PaperService
        from apps.services.paper.crawler_arxiv import ArXivCrawler

        mock_db = AsyncMock()
        mock_source = MagicMock()
        mock_source.id = "src-uuid-001"
        mock_source.name = "arxiv"

        mock_source_result = MagicMock()
        mock_source_result.scalars.return_value.first.return_value = mock_source

        mock_no_paper = MagicMock()
        mock_no_paper.scalars.return_value.first.return_value = None

        mock_db.execute = AsyncMock(side_effect=[mock_source_result, mock_no_paper])
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        mock_papers = [{
            "external_id": "arxiv:2507.12345",
            "title": "Advances in GPU Architecture",
            "published_at": date(2026, 7, 20),
            "category": "cs.AI",
            "metadata_json": {"abstract": "Test abstract", "authors": ["Smith"]}
        }]

        service = PaperService(mock_db)
        with patch.object(ArXivCrawler, "fetch_recent", new_callable=AsyncMock, return_value=mock_papers):
            count = await service.crawl_and_save_arxiv_recent(max_results=1)

        assert count == 1
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called()

    @pytest.mark.asyncio
    async def test_paper_service_skip_duplicate_paper(self):
        """이미 존재하는 논문은 업데이트만 하고 count에 포함되지 않아야 한다"""
        from apps.services.paper.paper_service import PaperService
        from apps.services.paper.crawler_arxiv import ArXivCrawler

        mock_db = AsyncMock()
        mock_source = MagicMock()
        mock_source.id = "src-uuid-001"
        mock_source.name = "arxiv"

        mock_existing_paper = MagicMock()
        mock_existing_paper.external_id = "arxiv:2507.12345"
        mock_existing_paper.metadata_json = {}

        mock_source_result = MagicMock()
        mock_source_result.scalars.return_value.first.return_value = mock_source

        mock_existing_result = MagicMock()
        mock_existing_result.scalars.return_value.first.return_value = mock_existing_paper

        mock_db.execute = AsyncMock(side_effect=[mock_source_result, mock_existing_result])
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()

        mock_papers = [{
            "external_id": "arxiv:2507.12345",
            "title": "Advances in GPU Architecture",
            "published_at": date(2026, 7, 20),
            "category": "cs.AI",
            "metadata_json": {"abstract": "Updated abstract"}
        }]

        service = PaperService(mock_db)
        with patch.object(ArXivCrawler, "fetch_recent", new_callable=AsyncMock, return_value=mock_papers):
            count = await service.crawl_and_save_arxiv_recent(max_results=1)

        assert count == 0
        mock_db.add.assert_not_called()
        assert mock_existing_paper.metadata_json == {"abstract": "Updated abstract"}
