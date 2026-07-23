import asyncio
import logging
from typing import List

from apps.worker.tasks.orchestrator import execute_extraction
from apps.worker.core.config import settings
from apps.services.retail.crawler import RetailUniversalCrawler
from apps.services.retail.crawler_enterprise import EnterpriseHardwareCrawler
from apps.services.financial.tasks import execute_financial_extraction
from apps.services.news.tasks import _run_3_tier_crawling

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GPU_PROVIDERS = [
    "vast-ai", "runpod", "aws", "vessl", "gpuaas",
    "cloudv", "runyourai", "gabia", "ktcloud"
]

async def run_gpu_crawlers(providers: List[str] = None):
    targets = providers or GPU_PROVIDERS
    logger.info(f"[BatchRunner] Running GPU crawlers for: {targets}")
    for provider in targets:
        try:
            await execute_extraction(provider)
        except Exception as e:
            logger.error(f"[BatchRunner] GPU crawler failed for {provider}: {e}")

async def run_retail_crawlers():
    logger.info("[BatchRunner] Running Retail & Enterprise crawlers...")
    try:
        retail_crawler = RetailUniversalCrawler()
        retail_data = await retail_crawler.execute_pipeline()
        logger.info(f"[BatchRunner] Retail crawler complete ({len(retail_data)} items).")
    except Exception as e:
        logger.error(f"[BatchRunner] Retail crawler failed: {e}")

    try:
        enterprise_crawler = EnterpriseHardwareCrawler()
        enterprise_data = await enterprise_crawler.execute_pipeline()
        logger.info(f"[BatchRunner] Enterprise crawler complete ({len(enterprise_data)} items).")
    except Exception as e:
        logger.error(f"[BatchRunner] Enterprise crawler failed: {e}")

async def run_financial_crawlers():
    logger.info("[BatchRunner] Running Financial crawlers...")
    for provider_slug in ["stock_market", "dram_futures"]:
        try:
            await execute_financial_extraction(provider_slug)
        except Exception as e:
            logger.error(f"[BatchRunner] Financial crawler failed for {provider_slug}: {e}")

async def run_news_crawlers():
    logger.info("[BatchRunner] Running News crawlers...")
    try:
        added = await _run_3_tier_crawling()
        logger.info(f"[BatchRunner] News crawler complete ({added} new articles).")
    except Exception as e:
        logger.error(f"[BatchRunner] News crawler failed: {e}")

async def run_batch(target: str = "all"):
    """
    Main entrypoint for manual batch trigger.
    Target options: 'all', 'gpu', 'retail', 'financial', 'news' or a specific GPU provider (e.g. 'aws')
    """
    target_lower = target.lower()
    logger.info(f"========== [BatchRunner STARTED] Target: '{target_lower}' ==========")

    if target_lower in ("all", "gpu"):
        await run_gpu_crawlers()
    elif target_lower in GPU_PROVIDERS:
        await run_gpu_crawlers([target_lower])

    if target_lower in ("all", "retail"):
        await run_retail_crawlers()

    if target_lower in ("all", "financial"):
        await run_financial_crawlers()

    if target_lower in ("all", "news"):
        await run_news_crawlers()

    logger.info(f"========== [BatchRunner FINISHED] Target: '{target_lower}' ==========")

if __name__ == "__main__":
    import sys
    target_arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    asyncio.run(run_batch(target_arg))
