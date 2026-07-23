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

@router.get("", response_model=Dict[str, Any])
async def get_latest_news(
    query: str = Query(None, description="검색어"),
    category: str = Query(None, description="카테고리 필터"),
    content_type: str = Query(None, description="콘텐츠 타입 (article, youtube)"),
    is_semiconductor_related: bool = Query(None, description="반도체 관련 여부"),
    source_id: str = Query(None, description="출처 ID 필터"),
    tag_id: str = Query(None, description="태그 ID 필터"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(30, ge=1, le=100, description="페이지당 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    """
    최신 글로벌 IT/반도체 뉴스 및 유튜브 목록을 반환합니다. (검색 및 필터 지원)
    """
    if db is None:
        return {"items": []}

    stmt = select(NewsArticle)

    if query:
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

    if source_id:
        stmt = stmt.where(NewsArticle.source_id == source_id)
        
    # 태그 필터 시 JOIN 필요
    if tag_id:
        from apps.services.news.models import NewsArticleTag
        stmt = stmt.join(NewsArticleTag, NewsArticle.id == NewsArticleTag.article_id).where(NewsArticleTag.tag_id == tag_id)

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
            "source_name": record.source_name, # 호환성
            "source_id": str(record.source_id) if record.source_id else None,
            "published_at": record.published_at.isoformat() if record.published_at else None,
            "summary": record.summary,
            "thumbnail_url": record.thumbnail_url,
            "content_type": record.content_type,
            "category": record.category,
            "is_semiconductor_related": record.is_semiconductor_related,
        })
        
    return {"items": news_list}

@router.get("/sources", response_model=List[Dict[str, Any]])
async def get_news_sources(db: AsyncSession = Depends(get_db)):
    """뉴스 수집 출처 목록"""
    from apps.services.news.models import NewsSource
    stmt = select(NewsSource).order_by(NewsSource.name)
    result = await db.execute(stmt)
    records = result.scalars().all()
    return [{"id": str(r.id), "name": r.name, "country": r.country} for r in records]

@router.get("/tags", response_model=List[Dict[str, Any]])
async def get_news_tags(db: AsyncSession = Depends(get_db)):
    """뉴스 태그 목록"""
    from apps.services.news.models import NewsTag
    stmt = select(NewsTag).order_by(NewsTag.name)
    result = await db.execute(stmt)
    records = result.scalars().all()
    return [{"id": str(r.id), "name": r.name, "category": r.category} for r in records]

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
    from apps.services.news.crawler import NewsAggregatorService
    aggregator = NewsAggregatorService()
    
    inserted_count = 0
    for item in normalized:
        success = await aggregator.upsert_article(db, item)
        if success:
            inserted_count += 1
            
    await db.commit()
    
    return {"status": "success", "fetched": len(normalized), "inserted": inserted_count}
