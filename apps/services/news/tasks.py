from apps.worker.celery_app import app
from apps.api.core.database import AsyncSessionLocal
from apps.services.news.models import NewsArticle

from apps.services.news.crawler_tier1_rss import NewsTier1Crawler
from apps.services.news.crawler_tier2_api import NewsTier2Crawler
from apps.services.news.crawler_tier3_browser import NewsTier3Crawler
from apps.services.news.crawler_youtube import YouTubeCrawler

import asyncio
import logging

logger = logging.getLogger(__name__)

async def _save_news_items(news_items):
    if not news_items or not AsyncSessionLocal:
        return 0
        
    async with AsyncSessionLocal() as session:
        added_count = 0
        for item in news_items:
            try:
                article = NewsArticle(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    source_name=item.get("source_name", ""),
                    published_at=item.get("published_at"),
                    summary=item.get("summary", ""),
                    author=item.get("author"),
                    thumbnail_url=item.get("thumbnail_url"),
                    language=item.get("language", "en"),
                    content_type=item.get("content_type", "article"),
                    is_semiconductor_related=item.get("is_semiconductor_related", False),
                    category=item.get("category"),
                    categories=item.get("categories", []),
                    matched_keywords=item.get("matched_keywords", ""),
                    collection_tier=item.get("collection_tier", "unknown")
                )
                session.add(article)
                await session.commit()
                added_count += 1
            except Exception as e:
                # Ignore unique constraint violations (duplicate URLs)
                await session.rollback()
                
        return added_count

async def _run_3_tier_crawling():
    total_added = 0
    TARGET_KEYWORD = "NVIDIA HBM"
    
    # Tier 1: Fastest and Safest
    logger.info("=== [Starting Tier 1 RSS Crawl] ===")
    t1_crawler = NewsTier1Crawler()
    t1_data = await t1_crawler.execute_pipeline()
    t1_added = await _save_news_items(t1_data)
    total_added += t1_added
    logger.info(f"[Tier 1] Added {t1_added} new articles.")
    
    # Check if we got enough relevant info (mock logic: if we didn't find the target keyword in Tier 1)
    found_target = any(TARGET_KEYWORD.lower() in item["title"].lower() for item in t1_data)
    
    if not found_target:
        # Tier 2: Fallback Global API
        logger.info(f"=== [Starting Tier 2 API Crawl] Keyword '{TARGET_KEYWORD}' not found in Tier 1. ===")
        t2_crawler = NewsTier2Crawler()
        t2_data = await t2_crawler.execute_pipeline()
        t2_added = await _save_news_items(t2_data)
        total_added += t2_added
        logger.info(f"[Tier 2] Added {t2_added} new articles.")
        
        found_target = any(TARGET_KEYWORD.lower() in item["title"].lower() for item in t2_data)
        
    if not found_target:
        # Tier 3: Hard-blocked exclusive sites using Headless Browser
        logger.warning(f"=== [Starting Tier 3 Playwright Scraper] Keyword '{TARGET_KEYWORD}' still missing. ===")
        t3_crawler = NewsTier3Crawler()
        t3_data = await t3_crawler.execute_pipeline()
        t3_added = await _save_news_items(t3_data)
        total_added += t3_added
        logger.info(f"[Tier 3] Added {t3_added} new articles.")
        logger.info(f"[Tier 3] Added {t3_added} new articles.")

    # YouTube Crawler (Always runs)
    logger.info("=== [Starting YouTube Crawler] ===")
    yt_crawler = YouTubeCrawler()
    yt_data = await yt_crawler.execute_pipeline()
    yt_added = await _save_news_items(yt_data)
    total_added += yt_added
    logger.info(f"[YouTube] Added {yt_added} new videos.")

    return total_added

@app.task(name="news.tick")
def execute_news_extraction():
    """매시간 마스터 스케줄러가 호출하는 글로벌 뉴스 다중 폴백 크롤링 Celery Task"""
    
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    total = loop.run_until_complete(_run_3_tier_crawling())
    logger.info(f"Global News Crawling completed. Total new articles: {total}")
    return f"Processed {total} news items across 3 tiers."
