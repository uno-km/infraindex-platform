import os
from celery import Celery
from celery.schedules import crontab

# Configure environment defaults
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")

broker_url = os.environ.get("REDIS_URL")
result_backend = os.environ.get("REDIS_URL")

# Create Celery App
celery_app = Celery(
    "infraindex_worker",
    broker=broker_url,
    backend=result_backend,
    include=["apps.batch.worker.tasks"]
)

# Optional configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=False,
)

# Setup Periodic Tasks (Celery Beat)
celery_app.conf.beat_schedule = {
    "tick-every-minute-for-dynamic-schedule": {
        "task": "orchestrator.tick",
        "schedule": crontab(minute="*"),
    },
    'crawl-news-every-30-minutes': {
        'task': 'tasks.crawl_all_news',
        'schedule': crontab(minute='*/30'),
    },
    'crawl-arxiv-every-6-hours': {
        'task': 'tasks.crawl_arxiv_papers',
        'schedule': crontab(minute='0', hour='*/6'),
    },
    'morning-report': {
        'task': 'tasks.generate_morning_report',
        'schedule': crontab(hour=7, minute=0),
    },
    'evening-report': {
        'task': 'tasks.generate_evening_report',
        'schedule': crontab(hour=18, minute=0),
    },
}
