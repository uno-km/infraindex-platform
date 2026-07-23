import asyncio
import logging

from apps.api.core.database import AsyncSessionLocal
from apps.services.news.crawler_tier1_rss import NewsTier1Crawler
from apps.services.market.crawler_retail import RetailCrawler
from apps.services.market.crawler_enterprise import EnterpriseCrawler

from apps.api.core.database import AsyncSessionLocal, init_db_engine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CrawlerRunner")

async def run_crawlers():
    init_db_engine()
    if AsyncSessionLocal is None:
        logger.error("DB Engine failed to initialize (USE_REAL_DB might be False). Exiting.")
        return
        
    async with AsyncSessionLocal() as db:
        logger.info("=== Starting News Crawler ===")
        news_crawler = NewsTier1Crawler()
        raw_news = await news_crawler.fetch_raw_data()
        parsed = news_crawler.parse_instances(raw_news)
        normalized = news_crawler.normalize_pricing(parsed)
        
        from apps.services.news.models import NewsArticle
        from sqlalchemy import select
        inserted = 0
        for item in normalized:
            stmt = select(NewsArticle).where(NewsArticle.url == item["url"])
            res = await db.execute(stmt)
            if not res.scalar_one_or_none():
                db.add(NewsArticle(**item))
                inserted += 1
        await db.commit()
        logger.info(f"News Crawler finished. Inserted {inserted} records.")
        
        logger.info("=== Starting Retail Crawler ===")
        retail_crawler = RetailCrawler()
        retail_res = await retail_crawler.sync_to_db(db)
        logger.info(f"Retail Crawler finished. {retail_res}")
        
        logger.info("=== Starting Enterprise Crawler ===")
        ent_crawler = EnterpriseCrawler()
        ent_res = await ent_crawler.sync_to_db(db)
        logger.info(f"Enterprise Crawler finished. {ent_res}")
        
        logger.info("All crawlers executed successfully!")

if __name__ == "__main__":
    asyncio.run(run_crawlers())
