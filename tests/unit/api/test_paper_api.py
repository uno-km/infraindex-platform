"""
tests/unit/api/test_paper_api.py
Phase 6 - ArXiv 페이퍼 API 유닛 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date


class TestPaperAPI:
    """페이퍼 API 엔드포인트 유닛 테스트"""

    def test_papers_router_importable(self):
        """papers router가 임포트 가능해야 한다"""
        from apps.server.api.v1.endpoints.papers import router
        assert router is not None

    def test_list_papers_route_exists(self):
        """GET /papers/ 라우트가 등록되어야 한다"""
        from apps.server.api.v1.endpoints.papers import router
        routes = [r.path for r in router.routes]
        assert len(routes) >= 1

    def test_crawl_trigger_route_exists(self):
        """POST /papers/crawl/arxiv 라우트가 등록되어야 한다"""
        from apps.server.api.v1.endpoints.papers import router
        routes = [r.path for r in router.routes]
        assert any("crawl" in r for r in routes), f"crawl 라우트 없음: {routes}"

    @pytest.mark.asyncio
    async def test_list_papers_db_none_returns_empty(self):
        """DB가 None일 때 빈 items 반환해야 한다"""
        from apps.server.api.v1.endpoints.papers import list_papers
        result = await list_papers(q=None, source=None, category=None, page=1, size=20, db=None)
        assert result == {"items": [], "total": 0, "page": 1, "size": 20}

    @pytest.mark.asyncio
    async def test_list_papers_with_mock_db(self):
        """DB 모킹으로 페이퍼 목록 조회 테스트"""
        from apps.server.api.v1.endpoints.papers import list_papers

        mock_paper = MagicMock()
        mock_paper.id = "paper-uuid-001"
        mock_paper.external_id = "arxiv:2507.12345"
        mock_paper.source = "arxiv"
        mock_paper.title = "Advances in GPU Architecture"
        mock_paper.title_ko = None
        mock_paper.published_at = date(2026, 7, 22)
        mock_paper.category = "cs.AI"
        mock_paper.citation_count = 0
        mock_paper.is_analyzed = False
        mock_paper.metadata_json = {}
        mock_paper.crawled_at = None

        mock_db = AsyncMock()

        # count query
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1

        # items query
        mock_items_result = MagicMock()
        mock_items_result.scalars.return_value.all.return_value = [mock_paper]

        mock_db.execute = AsyncMock(side_effect=[mock_count_result, mock_items_result])

        result = await list_papers(q=None, source=None, category=None, page=1, size=20, db=mock_db)

        assert "items" in result
        assert "total" in result
        assert result["total"] == 1

    @pytest.mark.asyncio
    async def test_trigger_crawl_arxiv_with_mock(self):
        """ArXiv 크롤 트리거 테스트 (PaperService 모킹)"""
        from apps.server.api.v1.endpoints.papers import trigger_crawl_arxiv

        mock_db = AsyncMock()

        with patch("apps.server.api.v1.endpoints.papers.PaperService") as mock_service_cls:
            mock_service = AsyncMock()
            mock_service.crawl_and_save_arxiv_recent = AsyncMock(return_value=5)
            mock_service_cls.return_value = mock_service

            result = await trigger_crawl_arxiv(max_results=10, db=mock_db)

        assert result["status"] == "success"
        assert result["new_papers_count"] == 5

    @pytest.mark.asyncio
    async def test_get_paper_not_found_raises_404(self):
        """존재하지 않는 paper_id로 조회 시 404가 발생해야 한다"""
        from apps.server.api.v1.endpoints.papers import get_paper
        from fastapi import HTTPException

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        with pytest.raises(HTTPException) as exc_info:
            await get_paper(paper_id="nonexistent-id", db=mock_db)

        assert exc_info.value.status_code == 404
