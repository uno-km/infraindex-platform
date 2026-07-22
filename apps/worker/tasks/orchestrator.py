import logging
import asyncio
from celery import shared_task
from apps.worker.core.alerts import send_critical_alert
from apps.worker.core.config import settings
from apps.worker.core.storage import get_storage
from apps.worker.providers.vast import VastCrawler
from apps.worker.providers.runpod import RunpodCrawler
from apps.worker.providers.aws import AWSCrawler

logger = logging.getLogger(__name__)

async def execute_extraction(provider_slug: str):
    """
    Pure Python function decoupled from Celery.
    Can be run locally or via Celery.
    """
    logger.info(f"[{provider_slug}] Factory extraction starting...")
    
    crawler = None
    if provider_slug == "vast-ai":
        crawler = VastCrawler()
    elif provider_slug == "runpod":
        crawler = RunpodCrawler()
    elif provider_slug == "aws":
        crawler = AWSCrawler()
    else:
        logger.error(f"Unknown provider: {provider_slug}")
        return

    try:
        normalized_data = await crawler.execute_pipeline()
        logger.info(f"[{provider_slug}] Successfully processed {len(normalized_data)} records.")
        
        # Save to abstracted storage (JSON or Postgres)
        storage = get_storage()
        await storage.save(provider_slug, normalized_data)
        
    except Exception as e:
        if settings.ENABLE_ALERTS:
            await send_critical_alert("Crawler Failed", str(e), provider_slug)
        logger.error(f"[{provider_slug}] Extraction failed: {str(e)}")
        raise e

# ----------------- Celery Tasks ----------------- #

@shared_task(name="orchestrator.tick")
def tick():
    """Called by Celery Beat every 5 minutes."""
    if not settings.USE_CELERY_QUEUE:
        logger.warning("Tick called but USE_CELERY_QUEUE is False.")
        return
        
    logger.info("Tick: Dispatching factory crawlers...")
    run_provider_collection.delay("vast-ai")
    run_provider_collection.delay("runpod")
    run_provider_collection.delay("aws")

@shared_task(
    name="orchestrator.run_provider_collection",
    autoretry_for=(Exception,), 
    retry_backoff=True, 
    retry_kwargs={'max_retries': 3}
)
def run_provider_collection(provider_slug: str):
    """Celery wrapper for the extraction function."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute_extraction(provider_slug))
