import asyncio
import logging
from apps.worker.tasks.orchestrator import execute_extraction
from apps.worker.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_all():
    """
    Serverless Entrypoint.
    Runs all crawlers sequentially without Celery or Redis.
    """
    logger.info(f"Starting Local Serverless Run (USE_REAL_DB={settings.USE_REAL_DB})")
    providers = ["vast-ai", "runpod", "aws"]
    
    for provider in providers:
        try:
            await execute_extraction(provider)
        except Exception as e:
            logger.error(f"Failed to process {provider}: {e}")
            
    logger.info("Local run completed.")

if __name__ == "__main__":
    asyncio.run(run_all())
