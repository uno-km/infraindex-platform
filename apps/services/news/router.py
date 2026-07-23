from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, or_
from typing import List, Dict, Any

from apps.api.core.database import get_db
from apps.services.news.models import NewsArticle

router = APIRouter()

# Note: Cache might need to vary by query params, but since query string can be anything, 
# caching the entire endpoint with arbitrary params might fill up the cache quickly or not work.
# We will remove the @cache decorator for this dynamic endpoint or leave it only for common queries.

@router.get("", response_model=List[Dict[str, Any]])
async def get_latest_news(
    query: str = Query(None, description="검색어"),
    category: str = Query(None, description="카테고리 필터"),
    content_type: str = Query(None, description="콘텐츠 타입 (article, youtube)"),
    is_semiconductor_related: bool = Query(None, description="반도체 관련 여부"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(30, ge=1, le=100, description="페이지당 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    """
    최신 글로벌 IT/반도체 뉴스 및 유튜브 목록을 반환합니다. (검색 및 필터 지원)
    """
    if db is None:
        return []

    stmt = select(NewsArticle)

    if query:
        # 간단한 ILIKE 검색 (Postgres 기준, SQLite도 호환됨)
        stmt = stmt.where(
            or_(
                NewsArticle.title.ilike(f"%{query}%"),
                NewsArticle.summary.ilike(f"%{query}%")
            )
        )
        
    if category:
        stmt = stmt.where(NewsArticle.category == category)
        
    if content_type:
        stmt = stmt.where(NewsArticle.content_type == content_type)
        
    if is_semiconductor_related is not None:
        stmt = stmt.where(NewsArticle.is_semiconductor_related == is_semiconductor_related)

    offset = (page - 1) * limit
    stmt = stmt.order_by(desc(NewsArticle.published_at)).offset(offset).limit(limit)
    
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    news_list = []
    for record in records:
        news_list.append({
            "id": str(record.id),
            "title": record.title,
            "url": record.url,
            "source": record.source_name,
            "published_at": record.published_at.isoformat() if record.published_at else None,
            "summary": record.summary,
            "thumbnail_url": record.thumbnail_url,
            "content_type": record.content_type,
            "category": record.category,
            "is_semiconductor_related": record.is_semiconductor_related,
            "matched_keywords": record.matched_keywords
        })
        
    return news_list

@router.post("/sync")
async def sync_news_from_crawler(db: AsyncSession = Depends(get_db)):
    """
    Trigger the RSS news crawler manually to fetch and insert real data.
    """
    from apps.services.news.crawler_tier1_rss import NewsTier1Crawler
    crawler = NewsTier1Crawler()
    
    # 1. Fetch raw data
    raw_data = await crawler.fetch_raw_data()
    
    # 2. Parse and classify
    parsed_data = crawler.parse_instances(raw_data)
    
    # 3. Normalize to our schema
    normalized = crawler.normalize_pricing(parsed_data)
    
    # 4. Insert into DB (Upsert / ignore duplicates)
    inserted_count = 0
    for item in normalized:
        # Check if URL exists
        stmt = select(NewsArticle).where(NewsArticle.url == item["url"])
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if not existing:
            new_article = NewsArticle(**item)
            db.add(new_article)
            inserted_count += 1
            
    await db.commit()
    
    return {"status": "success", "fetched": len(normalized), "inserted": inserted_count}
