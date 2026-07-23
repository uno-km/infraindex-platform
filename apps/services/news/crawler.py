import asyncio
import logging
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apps.services.news.models import NewsSource, NewsArticle, NewsTag, NewsArticleTag

logger = logging.getLogger(__name__)

class NewsAggregatorService:
    """
    뉴스 기사 및 소스/태그를 Upsert 하는 서비스 클래스
    """
    
    async def get_or_create_source(self, db: AsyncSession, source_name: str, country: str = "US") -> NewsSource:
        stmt = select(NewsSource).where(NewsSource.name == source_name)
        result = await db.execute(stmt)
        source = result.scalar_one_or_none()
        
        if not source:
            source = NewsSource(name=source_name, country=country)
            db.add(source)
            await db.flush()
        return source

    async def get_or_create_tag(self, db: AsyncSession, tag_name: str, category: str = None) -> NewsTag:
        stmt = select(NewsTag).where(NewsTag.name == tag_name)
        result = await db.execute(stmt)
        tag = result.scalar_one_or_none()
        
        if not tag:
            tag = NewsTag(name=tag_name, category=category)
            db.add(tag)
            await db.flush()
        return tag

    async def upsert_article(self, db: AsyncSession, item: Dict[str, Any]) -> bool:
        """
        주어진 크롤링 아이템을 DB에 적재합니다. (중복 검사 및 Source/Tag 연동)
        """
        # 1. Source 확인 및 생성
        source_name = item.get("source_name", "Unknown")
        source = await self.get_or_create_source(db, source_name)
        
        # 2. 기사 중복 검사
        stmt = select(NewsArticle).where(NewsArticle.url == item["url"])
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            return False # 이미 존재함
            
        # 3. 새로운 기사 삽입
        new_article = NewsArticle(
            title=item["title"],
            url=item["url"],
            source_id=str(source.id),
            source_name=source_name,
            published_at=item["published_at"],
            summary=item.get("summary", ""),
            content_type=item.get("content_type", "article"),
            is_semiconductor_related=item.get("is_semiconductor_related", False),
            category=item.get("categories", [])[0] if item.get("categories") else None,
            matched_keywords=",".join(item.get("matched_keywords", [])),
        )
        db.add(new_article)
        await db.flush()
        
        # 4. 태그 연동
        categories = item.get("categories", [])
        keywords = item.get("matched_keywords", [])
        
        # 카테고리 태그 
        for cat in categories:
            tag = await self.get_or_create_tag(db, cat, category="Category")
            db.add(NewsArticleTag(article_id=str(new_article.id), tag_id=str(tag.id)))
            
        # 키워드 태그
        for kw in keywords:
            tag = await self.get_or_create_tag(db, kw, category="Keyword")
            db.add(NewsArticleTag(article_id=str(new_article.id), tag_id=str(tag.id)))
            
        return True
