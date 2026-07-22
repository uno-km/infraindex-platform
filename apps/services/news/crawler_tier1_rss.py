import logging
import feedparser
import trafilatura
from typing import List, Dict, Any
from datetime import datetime, timezone
import asyncio

from apps.worker.providers.common.base import BaseProviderCrawler

logger = logging.getLogger(__name__)

class NewsTier1Crawler(BaseProviderCrawler):
    """
    Tier 1 Fallback Crawler: RSS & XML Sitemap Parser + Trafilatura Full-text Extraction.
    This is the fastest, safest, and most polite method to scrape news.
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
        from apps.api.core.database import AsyncSessionLocal
        from sqlalchemy import select
        from apps.api.models.system_config import CrawlerConfig
        
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
            # We use asyncio.to_thread because feedparser is blocking
            feed = await asyncio.to_thread(feedparser.parse, feed_info["url"])
            
            for entry in feed.entries[:5]: # Get top 5 per feed for demonstration
                raw_articles.append({
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": feed_info["source"]
                })
        
        return raw_articles

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        # In this tier, parsing includes downloading the full text and extracting it via Trafilatura.
        parsed = []
        for item in raw_data:
            logger.debug(f"[Tier 1] Extracting text for: {item['title']}")
            
            # Download and extract
            downloaded = trafilatura.fetch_url(item["url"])
            if downloaded:
                text = trafilatura.extract(downloaded)
            else:
                text = None
                
            parsed.append({
                "title": item["title"],
                "url": item["url"],
                "source": item["source"],
                "summary": text[:500] + "..." if text else None, # We use the first 500 chars as summary
                "published_at": item["published"]
            })
            
        return parsed

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Map to NewsArticle schema
        normalized = []
        for item in parsed_data:
            # Simple timestamp fallback
            dt = datetime.now(timezone.utc)
            
            normalized.append({
                "title": item["title"],
                "url": item["url"],
                "source": item["source"],
                "summary": item["summary"],
                "keywords": "semiconductor, tech", # Extracted or mocked keywords
                "published_at": dt,
                "collection_tier": "tier1_rss",
                "timestamp": dt
            })
        return normalized
