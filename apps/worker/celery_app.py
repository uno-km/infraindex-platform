from celery import Celery
from celery.schedules import crontab
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    "infraindex_worker",
    broker=redis_url,
    backend=redis_url,
    include=[
        "apps.worker.tasks.orchestrator",
        "apps.worker.tasks.outbox_publisher",  # P2-002: Outbox Publisher 등록
        "apps.worker.tasks.retail", # Retail price crawler
        "apps.worker.tasks.financial", # Financial market crawler
        "apps.worker.tasks.news", # News crawler
    ]
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
)

app.conf.beat_schedule = {
    # FIX-04: task명 수정 완료 (orchestrator.tick)
    # 수집 스케줄: 하루 3회 (09:00, 13:00, 18:00 UTC)
    "orchestrator-tick": {
        "task": "orchestrator.tick",
        "schedule": crontab(minute="0", hour="9,13,18"),
    },
    # P2-002: Outbox Publisher — 30초마다 미처리 이벤트 발행
    "outbox-publisher": {
        "task": "outbox.publish_pending",
        "schedule": 30.0,  # seconds
    },
    "retail_tick_hourly": {
        "task": "retail.tick",
        "schedule": crontab(minute="0"),
    },
    "market.tick": {
        "task": "market.tick",
        "schedule": crontab(minute="0"), # 매 시간 정각
    },
    "news.tick": {
        "task": "news.tick",
        "schedule": crontab(minute="0"), # 매 시간 정각에 뉴스 크롤링
    },
}
