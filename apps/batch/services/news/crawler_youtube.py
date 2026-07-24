import logging
import httpx
import os
from typing import List, Dict, Any
from datetime import datetime, timezone
import asyncio

from apps.batch.worker.providers.common.base import BaseProviderCrawler
from apps.batch.services.news.config import classify_article

logger = logging.getLogger(__name__)

class YouTubeCrawler(BaseProviderCrawler):
    """
    YouTube Data API v3 Crawler.
    """
    
    @property
    def provider_slug(self) -> str:
        return "youtube_api"

    async def fetch_raw_data(self) -> Any:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            logger.warning("[YouTubeCrawler] YOUTUBE_API_KEY is not set. Skipping YouTube crawling gracefully.")
            return []
            
        logger.info("[YouTubeCrawler] Fetching YouTube Videos via API...")
        raw_items = []
        
        # Keywords to search for
        search_queries = ["NVIDIA H100", "Semiconductor Market", "DRAM Price", "Data Center AI"]
        
        url = "https://www.googleapis.com/youtube/v3/search"
        
        async with httpx.AsyncClient() as client:
            for query in search_queries:
                try:
                    params = {
                        "part": "snippet",
                        "q": query,
                        "type": "video",
                        "order": "date",
                        "maxResults": 5, # Keep quota usage low
                        "key": api_key
                    }
                    response = await client.get(url, params=params, timeout=10.0)
                    response.raise_for_status()
                    data = response.json()
                    
                    for item in data.get("items", []):
                        snippet = item.get("snippet", {})
                        raw_items.append({
                            "video_id": item["id"].get("videoId"),
                            "title": snippet.get("title", ""),
                            "description": snippet.get("description", ""),
                            "channel_name": snippet.get("channelTitle", ""),
                            "published_at": snippet.get("publishedAt", ""),
                            "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                            "search_query": query
                        })
                except httpx.HTTPError as e:
                    logger.error(f"[YouTubeCrawler] HTTP Error for query '{query}': {e}")
                except Exception as e:
                    logger.error(f"[YouTubeCrawler] Error parsing YouTube API response: {e}")
                    
        return raw_items

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        parsed = []
        for item in raw_data:
            text_for_classification = f"{item['title']} {item['description']} {item['search_query']}"
            classification = classify_article(text_for_classification)
            
            parsed.append({
                "title": item["title"],
                "url": f"https://www.youtube.com/watch?v={item['video_id']}",
                "source_name": "YouTube",
                "author": item["channel_name"],
                "summary": item["description"],
                "thumbnail_url": item["thumbnail_url"],
                "published_at": item["published_at"],
                "classification": classification
            })
        return parsed

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for item in parsed_data:
            # Parse ISO 8601 published_at
            try:
                # "2024-05-15T12:00:00Z" -> datetime
                dt = datetime.fromisoformat(item["published_at"].replace("Z", "+00:00"))
            except:
                dt = datetime.now(timezone.utc)
                
            classification = item.get("classification", {})
            
            normalized.append({
                "title": item["title"],
                "url": item["url"],
                "source_name": item["source_name"],
                "summary": item["summary"],
                "author": item["author"],
                "thumbnail_url": item["thumbnail_url"],
                "published_at": dt,
                "collection_tier": "youtube_api",
                "is_semiconductor_related": classification.get("is_semiconductor_related", False),
                "category": classification.get("primary_category"),
                "categories": classification.get("categories", []),
                "matched_keywords": ",".join(classification.get("matched_keywords", [])),
                "content_type": "youtube"
            })
        return normalized
