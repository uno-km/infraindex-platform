import asyncio
from celery import shared_task
import logging
from apps.batch.services.ai_pricing.crawler_openrouter import crawl_openrouter_pricing
from apps.batch.services.ai_pricing.crawler_html import run_html_crawler

logger = logging.getLogger(__name__)

@shared_task(name="ai_pricing.crawl_daily_openrouter")
def task_crawl_ai_pricing():
    """
    매일 자정에 실행될 OpenRouter AI 모델 가격 크롤링 배치 작업
    """
    logger.info("Starting scheduled task: task_crawl_ai_pricing")
    try:
        updated_count = asyncio.run(crawl_openrouter_pricing())
        logger.info(f"Scheduled task completed. Updated {updated_count} models.")
        
        # Fallback for models not in OpenRouter (e.g., Anthropic official, Baidu)
        logger.info("Running HTML Fallback Crawler...")
        run_html_crawler()

        return {"status": "success", "updated_count": updated_count}
    except Exception as e:
        logger.error(f"Scheduled task failed: {e}")
        # The exceptions inside crawler_html are handled by @notify_on_error
        return {"status": "error", "message": str(e)}
