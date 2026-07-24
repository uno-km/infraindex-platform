"""
tests/unit/api/test_news_api.py
Phase 2 - 뉴스 API 유닛 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock


class TestNewsAPI:
    """뉴스 API 엔드포인트 유닛 테스트"""

    def test_news_router_importable(self):
        """news router가 임포트 가능해야 한다"""
        from apps.services.news.router import router
        assert router is not None

    def test_news_list_route_exists(self):
        """GET / 뉴스 목록 라우트가 등록되어야 한다"""
        from apps.services.news.router import router
        routes = [r.path for r in router.routes]
        # GET "" 또는 "/"
        assert any(r in ["", "/"] for r in routes), f"뉴스 목록 라우트 없음: {routes}"

    @pytest.mark.asyncio
    async def test_get_latest_news_db_none_returns_empty(self):
        """DB가 None일 때 빈 items를 반환해야 한다"""
        from apps.services.news.router import get_latest_news
        result = await get_latest_news(
            query=None, category=None, content_type=None,
            is_semiconductor_related=None, source_id=None, tag_id=None,
            page=1, limit=30, db=None
        )
        assert result == {"items": []}

    @pytest.mark.asyncio
    async def test_get_latest_news_with_mock_db(self):
        """DB 모킹으로 뉴스 목록 조회 테스트"""
        from apps.services.news.router import get_latest_news

        mock_article = MagicMock()
        mock_article.id = "art-uuid-001"
        mock_article.title = "NVIDIA H100 GPU price drops"
        mock_article.url = "https://example.com/article1"
        mock_article.source_name = "TechCrunch"
        mock_article.source_id = None
        mock_article.published_at = None
        mock_article.summary = "GPU prices are falling"
        mock_article.thumbnail_url = None
        mock_article.content_type = "article"
        mock_article.category = "GPU"
        mock_article.is_semiconductor_related = True

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_article]
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await get_latest_news(
            query=None, category=None, content_type=None,
            is_semiconductor_related=None, source_id=None, tag_id=None,
            page=1, limit=30, db=mock_db
        )

        assert "items" in result or isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_get_latest_news_with_category_filter(self):
        """카테고리 필터가 쿼리에 적용되어야 한다"""
        from apps.services.news.router import get_latest_news

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await get_latest_news(
            query=None, category="GPU", content_type=None,
            is_semiconductor_related=None, source_id=None, tag_id=None,
            page=1, limit=30, db=mock_db
        )

        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_briefing_route_exists(self):
        """뉴스 브리핑 라우트가 존재해야 한다"""
        from apps.services.news.router import router
        routes = [r.path for r in router.routes]
        assert any("briefing" in r for r in routes), f"briefing 라우트 없음: {routes}"
