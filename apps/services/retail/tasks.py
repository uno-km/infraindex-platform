from apps.worker.celery_app import app
from apps.services.retail.crawler import RetailUniversalCrawler
from apps.services.retail.crawler_enterprise import EnterpriseHardwareCrawler
from apps.worker.core.storage import PostgresStorage
import asyncio

@app.task(name="retail.tick")
def retail_tick():
    """
    Periodic task to crawl retail prices.
    Runs every hour as scheduled in celery_app.py.
    """
    # Create the crawler
    crawler = RetailUniversalCrawler()
    
    # Execute the pipeline
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    normalized_data = loop.run_until_complete(crawler.execute_pipeline())
    
    # Save the data
    crawler.save(normalized_data)
    
    return f"Processed {len(normalized_data)} retail items."

@app.task(name="enterprise.tick")
def enterprise_tick():
    """
    Periodic task to crawl B2B Enterprise AI Hardware prices.
    """
    crawler = EnterpriseHardwareCrawler()
    
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    normalized_data = loop.run_until_complete(crawler.execute_pipeline())
    
    # Enterprise crawler also uses PostgresStorage inherited from BaseCrawler
    crawler.save(normalized_data)
    
    return f"Processed {len(normalized_data)} enterprise items."
