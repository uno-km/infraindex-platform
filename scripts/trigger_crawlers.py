import asyncio
import logging
from apps.worker.core.config import settings
from apps.worker.tasks.orchestrator import execute_extraction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Only run the official API ones
    providers = ["vast-ai", "runpod", "aws"]
    
    logger.info("Starting manual execution of official API crawlers...")
    for provider in providers:
        try:
            await execute_extraction(provider)
            logger.info(f"Successfully finished extraction for {provider}")
        except Exception as e:
            logger.error(f"Failed to execute extraction for {provider}: {e}")
            
    # Run retail crawler
    from apps.worker.tasks.retail import retail_tick
    try:
        res = retail_tick()
        logger.info(f"Retail tick result: {res}")
    except Exception as e:
        logger.error(f"Failed retail tick: {e}")

if __name__ == "__main__":
    asyncio.run(main())
