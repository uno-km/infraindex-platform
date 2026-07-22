from celery import Celery
from celery.schedules import crontab
import os

# We would normally use config.py but setting it directly here for simplicity
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    "infraindex_worker",
    broker=redis_url,
    backend=redis_url,
    include=["apps.worker.tasks.orchestrator"]
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Worker 안전성 설정
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
)

# FIX-04: task명을 실제 @shared_task(name=...) 선언과 일치시킴
# orchestrator.py L47: @shared_task(name="orchestrator.tick")
app.conf.beat_schedule = {
    "orchestrator-tick": {
        "task": "orchestrator.tick",  # 수정: run_all_collections → tick
        "schedule": crontab(minute="*/5"),
    },
}
