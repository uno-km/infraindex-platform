import asyncio
import logging
import os
from sqlalchemy.ext.asyncio import AsyncSession
from apps.batch.services.market.crawler_retail import RetailCrawler
from shared.config.settings import settings

# Force REAL_DB
os.environ["USE_REAL_DB"] = "True"

logging.basicConfig(level=logging.INFO)

async def run_crawler():
    print(f"Using Naver Client ID: {settings.NAVER_SHOPPING_CLIENT_ID}")
    
    # Needs to be re-initialized because USE_REAL_DB was False
    from shared.db.session import _build_engine, _build_session_factory
    engine = _build_engine()
    SessionLocal = _build_session_factory(engine)
    
    from apps.batch.services.market.crawler_coupang import CoupangCrawler
    
    crawler = RetailCrawler()
    coupang = CoupangCrawler()
    
    async with SessionLocal() as db:
        print("Starting Naver Retail Crawler Sync...")
        result = await crawler.sync_to_db(db)
        print("Naver Sync result:", result)
        
        print("Starting Coupang Retail Crawler Sync...")
        coupang_res = await coupang.sync_to_db(db)
        print("Coupang Sync result:", coupang_res)

if __name__ == "__main__":
    asyncio.run(run_crawler())
