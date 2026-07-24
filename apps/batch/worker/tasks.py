import asyncio
import os
import sys
from celery import shared_task

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

@shared_task
def task_run_pipeline():
    """
    Run the full crawling and pre-computation pipeline.
    This task will be scheduled by Celery Beat every 8 hours.
    """
    print("Starting periodic full pipeline task...")
    
    # We can either run the script using os.system or import the main function
    # Importing is cleaner for MSA context
    from run_full_pipeline import main as run_pipeline
    
    try:
        # run_pipeline is an async function, we need to run it in an event loop
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        loop.run_until_complete(run_pipeline())
        print("Successfully finished pipeline task.")
        return {"status": "success"}
    except Exception as e:
        print(f"Error in pipeline task: {e}")
        return {"status": "error", "message": str(e)}

@shared_task(name="tasks.crawl_arxiv_papers")
def task_crawl_arxiv_papers():
    print("[Celery] Starting arxiv paper crawl task.")
    from apps.batch.services.paper.paper_service import PaperService
    from shared.db.session import AsyncSessionLocal
    import asyncio
    
    async def _do_crawl():
        async with AsyncSessionLocal() as session:
            service = PaperService(session)
            count = await service.crawl_and_save_arxiv_recent(max_results=50)
            return count

    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    new_count = loop.run_until_complete(_do_crawl())
    print(f"[Celery] Finished arxiv paper crawl task. New papers: {new_count}")

@shared_task
def task_generate_morning_report():
    """
    Generate morning report. Scheduled by Celery Beat.
    """
    from datetime import date
    from apps.batch.services.reporter.pdf_generator import PDFReporter
    
    reporter = PDFReporter()
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    try:
        file_path = loop.run_until_complete(reporter.generate_report(date.today(), "morning"))
        print(f"Successfully generated morning report: {file_path}")
        return {"status": "success", "file_path": file_path}
    except Exception as e:
        print(f"Error generating report: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}
