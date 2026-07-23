import logging
from sqlalchemy import select, exc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from apps.api.models.paper import PaperSource, PaperArticle
from apps.services.paper.crawler_arxiv import ArXivCrawler

logger = logging.getLogger(__name__)

class PaperService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_or_create_source(self, name: str, domain: str = None) -> PaperSource:
        stmt = select(PaperSource).where(PaperSource.name == name)
        result = await self.db.execute(stmt)
        source = result.scalars().first()
        
        if not source:
            source = PaperSource(name=name, domain=domain)
            self.db.add(source)
            await self.db.commit()
            await self.db.refresh(source)
            
        return source

    async def crawl_and_save_arxiv_recent(self, max_results: int = 50) -> int:
        crawler = ArXivCrawler()
        papers = await crawler.fetch_recent(max_results=max_results)
        
        if not papers:
            logger.info("[PaperService] No papers fetched from arXiv.")
            return 0
            
        source = await self._get_or_create_source(name="arxiv", domain="arxiv.org")
        
        new_count = 0
        for p_data in papers:
            stmt = select(PaperArticle).where(PaperArticle.external_id == p_data["external_id"])
            result = await self.db.execute(stmt)
            existing = result.scalars().first()
            
            if existing:
                # Update metadata if needed
                existing.metadata_json = p_data["metadata_json"]
            else:
                article = PaperArticle(
                    external_id=p_data["external_id"],
                    source=source.name,
                    source_id=source.id,
                    title=p_data["title"],
                    published_at=p_data["published_at"],
                    category=p_data["category"],
                    metadata_json=p_data["metadata_json"]
                )
                self.db.add(article)
                new_count += 1
                
        try:
            await self.db.commit()
            logger.info(f"[PaperService] Upserted {new_count} new arxiv papers.")
        except exc.SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"[PaperService] Failed to commit arxiv papers: {e}")
            return 0
            
        return new_count
