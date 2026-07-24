import logging
import feedparser
import trafilatura
from typing import List, Dict, Any
from datetime import datetime, timezone
import asyncio

from apps.batch.worker.providers.common.base import BaseProviderCrawler
from apps.batch.services.news.config import classify_article

logger = logging.getLogger(__name__)

class NewsTier1Crawler(BaseProviderCrawler):
    """
    Tier 1 Fallback Crawler: RSS & XML Sitemap Parser + Trafilatura Full-text Extraction.
    """
    
    @property
    def provider_slug(self) -> str:
        return "tier1_rss"

    # Some top tech & semiconductor feeds
    FEEDS = [
        {"source": "Bloomberg Tech", "url": "https://feeds.bloomberg.com/technology/news.xml"},
        {"source": "Reuters Tech", "url": "https://www.reutersagency.com/feed/?best-topics=tech&post_type=best"},
        {"source": "Hacker News", "url": "https://hnrss.org/frontpage"},
    ]

    async def fetch_raw_data(self) -> Any:
        logger.info("[Tier 1] Fetching RSS Feeds...")
        raw_articles = []
        
        # Load from DB instead of hardcoded
        feeds_to_fetch = self.FEEDS
        from shared.db.session import AsyncSessionLocal
        from sqlalchemy import select
        from shared.models.system_config import CrawlerConfig
        
        if AsyncSessionLocal:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(CrawlerConfig).where(CrawlerConfig.name == "tier1_rss"))
                cfg = result.scalar_one_or_none()
                if cfg and cfg.is_active and cfg.target_urls:
                    urls = [u.strip() for u in cfg.target_urls.split(",") if u.strip()]
                    if urls:
                        # Override hardcoded feeds
                        feeds_to_fetch = [{"source": "DB Configured", "url": u} for u in urls]
                elif cfg and not cfg.is_active:
                    logger.info("[Tier 1] Crawler is deactivated in DB. Skipping.")
                    return []
        
        for feed_info in feeds_to_fetch:
            feed = await asyncio.to_thread(feedparser.parse, feed_info["url"])
            
            for entry in feed.entries[:10]: # Get top 10
                raw_articles.append({
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "author": entry.get("author", ""),
                    "source": feed_info["source"]
                })
        
        return raw_articles

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        parsed = []
        for item in raw_data:
            logger.debug(f"[Tier 1] Extracting text for: {item['title']}")
            
            # Use basic parsing without slow trafilatura download for every item just to get summary
            # We will use the feed title for classification if trafilatura is slow
            text = None
            try:
                # trafilatura is synchronous, but we are inside a blocking function parse_instances
                downloaded = trafilatura.fetch_url(item["url"])
                if downloaded:
                    text = trafilatura.extract(downloaded)
            except Exception as e:
                logger.warning(f"Trafilatura failed for {item['url']}: {e}")
                
            summary = text[:500] + "..." if text else None
            
            # Classify
            classification = classify_article(item["title"] + " " + (summary or ""))
            
            parsed.append({
                "title": item["title"],
                "url": item["url"],
                "source_name": item["source"],
                "summary": summary,
                "author": item.get("author", None),
                "published_at": item["published"],
                "classification": classification
            })
            
        return parsed

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Map to NewsArticle schema
        normalized = []
        for item in parsed_data:
            dt = datetime.now(timezone.utc)
            classification = item.get("classification", {})
            
            normalized.append({
                "title": item["title"],
                "url": item["url"],
                "source_name": item["source_name"],
                "summary": item["summary"],
                "author": item.get("author", None),
                "published_at": dt, # In reality, parse item["published_at"] format
                "collection_tier": "tier1_rss",
                "is_semiconductor_related": classification.get("is_semiconductor_related", False),
                "category": classification.get("primary_category"),
                "categories": classification.get("categories", []),
                "matched_keywords": classification.get("matched_keywords", []),
                "content_type": "article"
            })
        return normalized
