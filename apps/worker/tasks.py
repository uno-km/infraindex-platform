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
