from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List, Dict, Any

from apps.api.core.database import get_db
from apps.services.news.models import NewsArticle

router = APIRouter()

@router.get("", response_model=List[Dict[str, Any]])
async def get_latest_news(
    limit: int = Query(50, description="불러올 뉴스의 최대 개수"),
    db: AsyncSession = Depends(get_db)
):
    """
    최신 글로벌 IT/반도체 뉴스 목록을 반환합니다.
    """
    stmt = select(
        NewsArticle.id,
        NewsArticle.title,
        NewsArticle.url,
        NewsArticle.source,
        NewsArticle.published_at,
        NewsArticle.summary,
        NewsArticle.keywords
    ).order_by(desc(NewsArticle.published_at)).limit(limit)
    
    result = await db.execute(stmt)
    records = result.all()
    
    news_list = []
    for record in records:
        news_list.append({
            "id": str(record.id),
            "title": record.title,
            "url": record.url,
            "source": record.source,
            "published_at": record.published_at.isoformat(),
            "summary": record.summary,
            "keywords": record.keywords
        })
        
    return news_list
