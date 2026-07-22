import logging
import asyncio
from celery import shared_task
from apps.worker.core.alerts import send_critical_alert
from apps.worker.providers.vast import VastCrawler
from apps.worker.providers.runpod import RunpodCrawler
from apps.worker.providers.aws import AWSCrawler

logger = logging.getLogger(__name__)

@shared_task(name="orchestrator.tick")
def tick():
    """Called by Celery Beat every 5 minutes."""
    logger.info("Tick: Dispatching factory crawlers...")
    run_provider_collection.delay("vast-ai")
    run_provider_collection.delay("runpod")
    run_provider_collection.delay("aws")

# 1. Exponential Backoff & Retry
@shared_task(
    name="orchestrator.run_provider_collection",
    autoretry_for=(Exception,), 
    retry_backoff=True, 
    retry_kwargs={'max_retries': 3}
)
def run_provider_collection(provider_slug: str):
    """
    Executes the crawler using the Factory Pattern.
    Automatically retries on exceptions with exponential backoff.
    """
    logger.info(f"[{provider_slug}] Factory extraction starting...")
    
    # 2. Factory Instantiation
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
        # Run async pipeline synchronously in Celery worker
        loop = asyncio.get_event_loop()
        normalized_data = loop.run_until_complete(crawler.execute_pipeline())
        logger.info(f"[{provider_slug}] Successfully processed {len(normalized_data)} records.")
        
        # Next step: Save to PriceHistory (implemented in DB model step)
        
    except Exception as e:
        # 3. Critical Alerting (Discord/Telegram)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            send_critical_alert("Crawler Failed", str(e), provider_slug)
        )
        logger.error(f"[{provider_slug}] Extraction failed: {str(e)}")
        raise e  # Reraise to trigger Celery retry
