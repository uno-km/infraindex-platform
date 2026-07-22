import sys
import logging
from apps.worker.core.config import settings
from apps.worker.tasks.orchestrator import execute_extraction

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("run_local")

def main():
    """
    Entrypoint for serverless/cron environments.
    Bypasses Celery completely and runs extraction sequentially.
    """
    if settings.USE_CELERY_QUEUE:
        logger.warning("USE_CELERY_QUEUE is True, but you are running the local script. Are you sure?")
        
    providers = ["vast-ai", "runpod", "aws"]
    
    logger.info("Starting local extraction run for all providers...")
    for provider in providers:
        try:
            execute_extraction(provider)
        except Exception as e:
            logger.error(f"Failed to extract from {provider}: {e}")
            # Continue to next provider even if one fails
            continue
            
    logger.info("Local extraction run complete!")

if __name__ == "__main__":
    main()
