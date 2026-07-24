import logging
import asyncio
from datetime import datetime, timezone
from celery import shared_task
from apps.batch.worker.core.config import settings
from apps.batch.worker.core.storage import get_storage
from apps.batch.services.financial.crawler import StockMarketCrawler, DramFuturesCrawler

logger = logging.getLogger(__name__)

async def execute_financial_extraction(provider_slug: str):
    logger.info(f"[{provider_slug}] Financial extraction starting...")
    
    if provider_slug == "stock_market":
        crawler = StockMarketCrawler()
    elif provider_slug == "dram_futures":
        crawler = DramFuturesCrawler()
    else:
        logger.error(f"Unknown financial provider: {provider_slug}")
        return

    try:
        raw_normalized = await crawler.execute_pipeline()
        logger.info(f"[{provider_slug}] Extraction complete: {len(raw_normalized)} records.")
        
        # Save to real DB if needed
        storage = get_storage()
        # Storage doesn't have an explicit save_financial method yet, we'll update storage.py or just use SQLAlchemy directly for now
        if settings.USE_REAL_DB and settings.DATABASE_URL:
            from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
            from apps.batch.services.financial.models import FinMktHistory
            
            db_url = settings.DATABASE_URL
            if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
                db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

            engine = create_async_engine(db_url, echo=False, future=True, pool_size=2, max_overflow=5)
            SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
            
            async with SessionLocal() as db:
                async with db.begin():
                    for item in raw_normalized:
                        record = FinMktHistory(
                            sym_cd=item["symbol"],
                            ast_typ=item["asset_type"],
                            opn_prc=item["open"],
                            hi_prc=item["high"],
                            lo_prc=item["low"],
                            cls_prc=item["close"],
                            vol_cnt=item.get("volume"),
                            crncy_cd=item.get("currency", "USD"),
                            ts=datetime.now(timezone.utc)
                        )
                        db.add(record)
            await engine.dispose()
            logger.info(f"[{provider_slug}] Data committed to DB.")
        else:
            crawler.save(raw_normalized)

    except Exception as e:
        logger.error(f"[{provider_slug}] Extraction failed: {e}", exc_info=True)

@shared_task(name="market.tick")
def market_tick():
    if not settings.USE_CELERY_QUEUE:
        logger.warning("market.tick called but USE_CELERY_QUEUE is False.")
        return

    logger.info("Market Tick: Dispatching financial crawlers...")
    run_financial_collection.delay("stock_market")
    run_financial_collection.delay("dram_futures")

@shared_task(name="market.run_financial_collection")
def run_financial_collection(provider_slug: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(execute_financial_extraction(provider_slug))
    finally:
        loop.close()
