"""
tests/services/NWS-003_news_crawler_test.py
Phase 2 - Crawler & Service Tagging Logic Tests
"""
import pytest
from datetime import datetime, timezone
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.mark.asyncio
async def test_classify_article_with_heuristic():
    """휴리스틱 태깅 함수 검증"""
    from apps.batch.services.news.config import classify_article
    text = "NVIDIA announced the new H100 GPU and HBM3e memory"
    result = classify_article(text)
    
    assert result["is_semiconductor_related"] is True
    assert "GPU" in result["categories"]
    assert "메모리" in result["categories"]
    assert "h100" in result["matched_keywords"]
    assert "hbm3e" in result["matched_keywords"]

@pytest.mark.asyncio
async def test_crawler_upsert_logic():
    """크롤러가 DB에 Source와 Tag를 Upsert 하는 로직 테스트"""
    # This is an integration/logic test mock
    from shared.models import NewsSource, NewsTag, NewsArticle
    
    mock_db = AsyncMock()
    
    # 1. Mock select Source
    mock_source = MagicMock()
    mock_source.id = uuid.uuid4()
    mock_source_result = MagicMock()
    mock_source_result.scalar_one_or_none.return_value = mock_source
    
    # 2. Mock select Article
    mock_article_result = MagicMock()
    mock_article_result.scalar_one_or_none.return_value = None  # New article
    
    # 3. Mock select Tag
    mock_tag = MagicMock()
    mock_tag.id = uuid.uuid4()
    mock_tag_result = MagicMock()
    mock_tag_result.scalar_one_or_none.return_value = mock_tag
    
    # 순서대로 execute 반환값 지정
    mock_db.execute.side_effect = [
        mock_source_result,  # find source
        mock_article_result, # check article
        mock_tag_result,     # check tag 1 (Category: GPU)
        mock_tag_result,     # check tag 2 (Category: 메모리)
        mock_tag_result,     # check tag 3 (Keyword: nvidia)
        mock_tag_result      # check tag 4 (Keyword: memory)
    ]
    
    item = {
        "title": "Nvidia memory",
        "url": "http://test.com/1",
        "source_name": "Tech News",
        "categories": ["GPU", "메모리"],
        "matched_keywords": ["nvidia", "memory"],
        "content_type": "article",
        "published_at": datetime.now(timezone.utc),
        "is_semiconductor_related": True
    }
    
    from apps.batch.services.news.crawler import NewsAggregatorService
    service = NewsAggregatorService()
    
    # Service 함수 호출
    result = await service.upsert_article(mock_db, item)
    
    assert result is True
    assert mock_db.add.call_count > 0  # Article, ArticleTags 등이 add 되어야 함
