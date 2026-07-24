import asyncio
import logging
from datetime import datetime, timezone
import traceback
from typing import List, Dict

from apps.batch.worker.core.config import settings
from apps.batch.worker.tasks.orchestrator import _insert_history
from apps.batch.services.retail.crawler import RetailUniversalCrawler
from apps.batch.services.retail.crawler_enterprise import EnterpriseHardwareCrawler
from apps.batch.services.financial.tasks import execute_financial_extraction
from apps.batch.services.news.tasks import _run_3_tier_crawling
from apps.batch.worker.tasks.orchestrator import execute_extraction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_dtl_job(bat_id: str, job_id: str, provider_slug: str):
    logger.info(f"[{bat_id}/{job_id}] Execution starting... (Provider: {provider_slug})")
    start_dt = datetime.now(timezone.utc).replace(tzinfo=None)
    
    try:
        # 분기 처리 (provider_slug)
        if bat_id == "GPU_DATA_CRAWLING":
            await execute_extraction(provider_slug)
        elif bat_id == "RETAIL_DATA_CRAWLING":
            from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
            
            db_url = settings.DATABASE_URL
            if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
                db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            engine = create_async_engine(db_url, echo=False, future=True)
            SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
            
            if provider_slug == "naver":
                from apps.batch.services.market.crawler_retail import RetailCrawler
                crawler = RetailCrawler()
                async with SessionLocal() as db:
                    res = await crawler.sync_to_db(db)
                    logger.info(f"[naver] result: {res}")
            elif provider_slug == "coupang":
                from apps.batch.services.market.crawler_coupang import CoupangCrawler
                crawler = CoupangCrawler()
                async with SessionLocal() as db:
                    res = await crawler.sync_to_db(db)
                    logger.info(f"[coupang] result: {res}")
            await engine.dispose()
        elif bat_id == "FINANCIAL_DATA_CRAWLING":
            await execute_financial_extraction(provider_slug)
        elif bat_id == "NEWS_DATA_CRAWLING":
            await _run_3_tier_crawling()
        else:
            logger.warning(f"Unknown bat_id: {bat_id}")
            
        end_dt = datetime.now(timezone.utc).replace(tzinfo=None)
        await _insert_history(bat_id, job_id, start_dt, end_dt, "SUCCESS")
        elapsed = (end_dt - start_dt).total_seconds()
        logger.info(f"[{bat_id}/{job_id}] Execution SUCCESS. (Elapsed: {elapsed:.2f}s)")
    except Exception as e:
        end_dt = datetime.now(timezone.utc).replace(tzinfo=None)
        err_trace = traceback.format_exc()
        await _insert_history(bat_id, job_id, start_dt, end_dt, "FAIL", err_trace)
        elapsed = (end_dt - start_dt).total_seconds()
        logger.error(f"[{bat_id}/{job_id}] Execution FAIL: {e} (Elapsed: {elapsed:.2f}s)")

async def _get_jobs_from_db(target: str) -> List[Dict[str, str]]:
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
    from sqlalchemy import select
    from shared.models.batch_schedule import SysBatSchDtl
    from apps.batch.worker.core.config import settings as worker_settings
    
    db_url = worker_settings.DATABASE_URL
    if not db_url:
        from shared.config.settings import settings as api_settings
        db_url = api_settings.async_database_uri
        
    if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    engine = create_async_engine(db_url, echo=False, future=True)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    
    target_lower = target.lower()
    
    target_to_bat_id = {
        "gpu": "GPU_DATA_CRAWLING",
        "retail": "RETAIL_DATA_CRAWLING",
        "financial": "FINANCIAL_DATA_CRAWLING",
        "news": "NEWS_DATA_CRAWLING"
    }

    jobs = []
    async with SessionLocal() as session:
        stmt = select(SysBatSchDtl).where(SysBatSchDtl.use_yn == "Y")
        
        if target_lower != "all":
            if target_lower in target_to_bat_id:
                stmt = stmt.where(SysBatSchDtl.bat_id == target_to_bat_id[target_lower])
            else:
                # 특정 provider_slug (예: 'aws', 'vast-ai')
                stmt = stmt.where(SysBatSchDtl.ref_val_1 == target_lower)
                
        # run_ord 순으로 정렬
        stmt = stmt.order_by(SysBatSchDtl.bat_id, SysBatSchDtl.run_ord)
        
        result = await session.execute(stmt)
        dtls = result.scalars().all()
        
        for dtl in dtls:
            if dtl.ref_val_1:
                jobs.append({
                    "bat_id": dtl.bat_id,
                    "job_id": dtl.job_id,
                    "slug": dtl.ref_val_1
                })
                
    await engine.dispose()
    return jobs

async def run_batch(target: str = "all"):
    """
    Main entrypoint for manual batch trigger.
    Target options: 'all', 'gpu', 'retail', 'financial', 'news' or a specific GPU provider (e.g. 'aws')
    """
    target_lower = target.lower()
    logger.info(f"========== [BatchRunner STARTED] Target: '{target_lower}' ==========")

    # 1. Target 매핑 (DB에서 동적 조회)
    jobs = await _get_jobs_from_db(target_lower)
    
    if not jobs:
        logger.warning(f"No jobs found for target: {target_lower}")
        return

    logger.info(f"Loaded {len(jobs)} jobs to execute from DB.")

    # 2. 순차 실행 (히스토리 로깅 포함)
    for j in jobs:
        await run_dtl_job(j["bat_id"], j["job_id"], j["slug"])

    logger.info(f"========== [BatchRunner FINISHED] Target: '{target_lower}' ==========")

if __name__ == "__main__":
    import sys
    target_arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    asyncio.run(run_batch(target_arg))
