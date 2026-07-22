import logging
import asyncio
from celery import shared_task
from apps.worker.core.alerts import send_critical_alert
from apps.worker.providers.vast import VastCrawler
from apps.worker.providers.runpod import RunpodCrawler
from apps.worker.providers.aws import AWSCrawler
from apps.worker.core.config import settings
from apps.worker.core.storage import get_storage_backend

logger = logging.getLogger(__name__)

def execute_extraction(provider_slug: str):
    """
    Core business logic for extraction, decoupled from Celery.
    Can be run via Celery or locally via a simple script.
    """
    logger.info(f"[{provider_slug}] Factory extraction starting...")
    
    # 1. Factory Instantiation
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
        # Run async pipeline synchronously (since celery/cron blocks)
        loop = asyncio.get_event_loop()
        normalized_data = loop.run_until_complete(crawler.execute_pipeline())
        logger.info(f"[{provider_slug}] Successfully processed {len(normalized_data)} records.")
        
        # 2. Storage Injection
        storage = get_storage_backend(settings.USE_REAL_DB)
        loop.run_until_complete(storage.save(provider_slug, normalized_data))
        
    except Exception as e:
        # 3. Alerting Toggle
        if settings.ENABLE_ALERTS:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                send_critical_alert("Crawler Failed", str(e), provider_slug)
            )
        logger.error(f"[{provider_slug}] Extraction failed: {str(e)}")
        raise e

# -------------------------------------------------------------------
# Celery Wrappers (Only used if settings.USE_CELERY_QUEUE is True)
# -------------------------------------------------------------------

@shared_task(name="orchestrator.tick")
def tick():
    """Called by Celery Beat every 5 minutes."""
    logger.info("Tick: Dispatching factory crawlers...")
    # If Celery is enabled, we delay. Otherwise, this file can just be imported and run.
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
    """
    Celery wrapper that automatically retries on exceptions with exponential backoff.
    """
    execute_extraction(provider_slug)
