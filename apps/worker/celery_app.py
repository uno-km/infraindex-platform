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
        "apps.services.retail.tasks", # Retail price crawler
        "apps.services.financial.tasks", # Financial market crawler
        "apps.services.news.tasks", # News crawler
    ]
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=False,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
)

# 마스터 스케줄러: 배치 작업들이 서로 꼬이지 않도록 순차적(Staggered)으로 큐에 적재합니다.
@app.task(name="master.tick")
def master_tick():
    # 0분: 클라우드 인프라 가격 (GPU, CPU) 크롤링
    app.send_task("orchestrator.tick", countdown=0)
    
    # 2분 뒤: 리테일 하드웨어 가격 (RAM, CPU, Retail GPU) 크롤링
    app.send_task("retail.tick", countdown=120)
    
    # 4분 뒤: 금융 시장 데이터 (주식, 선물) 크롤링
    app.send_task("market.tick", countdown=240)
    
    # 6분 뒤: 글로벌 뉴스 크롤링
    app.send_task("news.tick", countdown=360)
    
    # 8분 뒤: 초고가 기업용 하드웨어(B2B) 장비 가격 크롤링
    app.send_task("enterprise.tick", countdown=480)


app.conf.beat_schedule = {
    # 수집 스케줄: 하루 3회 (09:00, 15:00, 18:00 KST) - 마스터 스케줄러가 일괄 통제
    "master-tick": {
        "task": "master.tick",
        "schedule": crontab(minute="0", hour="9,15,18"),
    },
    # P2-002: Outbox Publisher — 30초마다 미처리 이벤트 발행 (이건 독립적으로 상시 동작)
    "outbox-publisher": {
        "task": "outbox.publish_pending",
        "schedule": 30.0,  # seconds
    },
}
