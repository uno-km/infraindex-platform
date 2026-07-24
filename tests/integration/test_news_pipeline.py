"""
tests/integration/test_news_pipeline.py
Phase 2 - 뉴스 수집 -> 분류 -> DB 저장 파이프라인 통합 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestNewsPipeline:
    """뉴스 크롤러 -> 분류기 -> DB 저장 -> 알림 체크 파이프라인 통합 테스트"""

    def test_classify_then_map_to_tags(self):
        """classify_article 결과가 뉴스 태그 형식과 호환되어야 한다"""
        from apps.services.news.config import classify_article

        article_text = "NVIDIA H100 GPU cloud rental prices fall as competition increases"
        classification = classify_article(article_text)

        assert classification["is_semiconductor_related"] is True
        assert isinstance(classification["categories"], list)
        assert isinstance(classification["matched_keywords"], list)

        tags = [{"name": cat, "category": "auto"} for cat in classification["categories"]]
        assert all("name" in tag for tag in tags)

    def test_classify_unrelated_article(self):
        """무관한 기사는 분류되지 않아야 한다"""
        from apps.services.news.config import classify_article

        article_text = "Seoul opens new public park near Han River"
        result = classify_article(article_text)
        assert result["is_semiconductor_related"] is False

    @pytest.mark.asyncio
    async def test_news_keyword_alert_triggers_on_crawl(self):
        """크롤된 뉴스가 알림 키워드에 매칭되면 AlertEngine이 트리거되어야 한다"""
        from apps.services.alerts.alert_engine import AlertEngine

        mock_db = AsyncMock()
        mock_rule = MagicMock()
        mock_rule.alert_type = "news_keyword"
        mock_rule.target = "HBM4"
        mock_rule.is_active = True

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_rule]
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()

        mock_article = MagicMock()
        mock_article.title = "SK Hynix announces HBM4 production ramp-up for 2026"
        mock_article.url = "https://example.com/hbm4-news"

        engine = AlertEngine()
        alerts = await engine.check_news_alerts(db=mock_db, article=mock_article)

        assert len(alerts) == 1
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_news_keyword_alert_no_match(self):
        """뉴스 제목에 알림 키워드가 없으면 알림이 트리거되지 않아야 한다"""
        from apps.services.alerts.alert_engine import AlertEngine

        mock_db = AsyncMock()
        mock_rule = MagicMock()
        mock_rule.alert_type = "news_keyword"
        mock_rule.target = "HBM4"
        mock_rule.is_active = True

        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_rule]
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.add = MagicMock()

        mock_article = MagicMock()
        mock_article.title = "Restaurant opens new Seoul branch"
        mock_article.url = "https://example.com/unrelated-news"

        engine = AlertEngine()
        alerts = await engine.check_news_alerts(db=mock_db, article=mock_article)

        assert len(alerts) == 0
        mock_db.add.assert_not_called()

    def test_paper_service_importable_without_circular_import(self):
        """PaperService는 순환 임포트 없이 임포트 가능해야 한다"""
        from apps.services.paper.paper_service import PaperService
        assert PaperService is not None

    @pytest.mark.asyncio
    async def test_paper_upsert_on_new_paper(self):
        """새 논문은 DB에 add되어야 한다"""
        from apps.services.paper.paper_service import PaperService
        from apps.services.paper.crawler_arxiv import ArXivCrawler

        mock_db = AsyncMock()
        mock_source = MagicMock()
        mock_source.id = "src-001"
        mock_source.name = "arxiv"

        # source 조회 성공
        mock_source_result = MagicMock()
        mock_source_result.scalars.return_value.first.return_value = mock_source

        # paper 조회: 없음
        mock_no_paper = MagicMock()
        mock_no_paper.scalars.return_value.first.return_value = None

        mock_db.execute = AsyncMock(side_effect=[mock_source_result, mock_no_paper])
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        mock_papers = [{
            "external_id": "arxiv:2507.99999",
            "title": "New Paper",
            "published_at": None,
            "category": "cs.AI",
            "metadata_json": {"abstract": "test"}
        }]

        service = PaperService(mock_db)
        with patch.object(ArXivCrawler, "fetch_recent", new_callable=AsyncMock, return_value=mock_papers):
            count = await service.crawl_and_save_arxiv_recent(max_results=1)

        assert count == 1
        mock_db.add.assert_called_once()
