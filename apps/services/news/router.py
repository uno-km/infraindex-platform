from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List, Dict, Any

from apps.api.core.database import get_db
from apps.services.news.models import NewsArticle

router = APIRouter()

from fastapi_cache.decorator import cache

@router.get("", response_model=List[Dict[str, Any]])
@cache(expire=3600 * 8)
async def get_latest_news(
    limit: int = Query(50, description="불러올 뉴스의 최대 개수"),
    db: AsyncSession = Depends(get_db)
):
    """
    최신 글로벌 IT/반도체 뉴스 목록을 반환합니다.
    """
    if db is None:
        return []

    stmt = select(
        NewsArticle.id,
        NewsArticle.titl_nm,
        NewsArticle.arti_url,
        NewsArticle.src_nm,
        NewsArticle.pub_ts,
        NewsArticle.sum_txt,
        NewsArticle.kwd_txt
    ).order_by(desc(NewsArticle.pub_ts)).limit(limit)
    
    result = await db.execute(stmt)
    records = result.all()
    
    news_list = []
    for record in records:
        news_list.append({
            "id": str(record.id),
            "title": record.titl_nm,
            "url": record.arti_url,
            "source": record.src_nm,
            "published_at": record.pub_ts.isoformat() if record.pub_ts else None,
            "summary": record.sum_txt,
            "keywords": record.kwd_txt
        })
        
    return news_list
