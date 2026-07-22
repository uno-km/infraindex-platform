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
)

app.conf.beat_schedule = {
    # Instead of static hourly runs, the orchestrator ticks every 5 minutes
    # and checks the `ScheduleConfig` table to dispatch dynamic jobs.
    "orchestrator-tick": {
        "task": "orchestrator.run_all_collections",
        "schedule": crontab(minute="*/5"),
    },
}
