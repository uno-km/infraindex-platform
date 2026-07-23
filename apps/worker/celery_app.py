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
    include=["apps.worker.tasks"]
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
    # 매 1분마다 DB 싱글턴 메모리 일정을 검사
    "tick-every-minute-for-dynamic-schedule": {
        "task": "orchestrator.tick",
        "schedule": crontab(minute="*"),
    },
}
