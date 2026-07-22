from apps.worker.core.celery_app import celery_app
from apps.api.core.database import SessionLocal
from apps.worker.providers.news import GlobalNewsCrawler
from apps.api.models.news import NewsArticle
import asyncio
import logging

logger = logging.getLogger(__name__)

async def _crawl_and_save_news():
    crawler = GlobalNewsCrawler()
    news_items = await crawler.crawl()
    
    if not news_items:
        logger.info("No news items extracted.")
        return
        
    async with SessionLocal() as session:
        added_count = 0
        for item in news_items:
            try:
                # 존재하는지 확인 (url 기준)
                # 이부분은 단순 트라이캐치로 중복 방지 (unique 제약조건)
                article = NewsArticle(
                    title=item["title"],
                    url=item["url"],
                    source=item["source"],
                    published_at=item["published_at"],
                    summary=item.get("summary", ""),
                    keywords=item.get("keywords", "")
                )
                session.add(article)
                await session.commit()
                added_count += 1
            except Exception as e:
                # UNIQUE constraint 방지 등
                await session.rollback()
                
        logger.info(f"Successfully added {added_count} new articles to DB.")

@celery_app.task(name="news.tick")
def execute_news_extraction():
    """매시간 정각에 글로벌 뉴스를 크롤링하는 Celery Task"""
    from apps.api.core.config import settings
    
    if not settings.USE_REAL_DB:
        logger.warning("USE_REAL_DB=False, skipping news persistence.")
        return
        
    asyncio.run(_crawl_and_save_news())
