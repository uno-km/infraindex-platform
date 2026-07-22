import logging
from typing import List, Dict, Any
from datetime import datetime, timezone
import asyncio

from apps.worker.providers.common.base import BaseProviderCrawler

logger = logging.getLogger(__name__)

class NewsTier2Crawler(BaseProviderCrawler):
    """
    Tier 2 Fallback Crawler: Global News API (e.g., NewsAPI, GDELT, Bing News).
    Used when specific keywords are not found in Tier 1 RSS feeds.
    """
    
    @property
    def provider_slug(self) -> str:
        return "tier2_api"

    async def fetch_raw_data(self) -> Any:
        logger.info("[Tier 2] Querying Global News API for missing keywords...")
        
        # Simulating an API response from a service like NewsAPI for the keyword "NVIDIA HBM"
        # In production, this would make an HTTP request using self.http
        await asyncio.sleep(0.5)
        
        return {
            "status": "ok",
            "totalResults": 2,
            "articles": [
                {
                    "title": "NVIDIA's Next Gen HBM Chips Facing Supply Bottlenecks",
                    "url": "https://example-global-news.com/nvidia-hbm",
                    "source": {"name": "Tech Global News"},
                    "description": "The latest report indicates that NVIDIA is struggling with HBM yields...",
                    "publishedAt": "2026-07-22T10:00:00Z"
                },
                {
                    "title": "SK Hynix Secures Massive HBM Order",
                    "url": "https://example-asia-news.com/sk-hynix",
                    "source": {"name": "Asia Biz"},
                    "description": "SK Hynix has reportedly locked in orders for the next two years...",
                    "publishedAt": "2026-07-22T09:30:00Z"
                }
            ]
        }

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        if not raw_data or raw_data.get("status") != "ok":
            return []
            
        return raw_data.get("articles", [])

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for item in parsed_data:
            dt = datetime.now(timezone.utc)
            
            normalized.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "source": item.get("source", {}).get("name", "Unknown API Source"),
                "summary": item.get("description"),
                "keywords": "HBM, NVIDIA, SK Hynix", 
                "published_at": dt, # In reality, parse item.get("publishedAt")
                "collection_tier": "tier2_api",
                "timestamp": dt
            })
        return normalized
