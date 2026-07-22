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

@app.task(name="master.tick")
def master_tick():
    """
    마스터 틱은 이제 DB의 CrawlerConfig를 확인하여 is_active=True인 크롤러만 동작시킵니다.
    주기(interval_minutes)를 고려하려면 스케줄러 자체를 커스텀해야 하지만, 
    여기서는 단순하게 활성화 여부만 읽어 순차 큐잉을 진행합니다.
    """
    import asyncio
    from apps.api.core.database import AsyncSessionLocal
    from sqlalchemy import select
    from apps.api.models.system_config import CrawlerConfig
    
    async def fetch_configs():
        if AsyncSessionLocal:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(CrawlerConfig))
                return result.scalars().all()
        return []
    
    try:
        # FastAPI와 같은 프로세스가 아니므로 새 이벤트 루프 생성 필요
        loop = asyncio.get_event_loop()
        configs = loop.run_until_complete(fetch_configs())
    except Exception:
        configs = []
        
    active_configs = {c.name: c for c in configs if c.is_active} if configs else {}
    
    # 0분: 클라우드 인프라 가격 (GPU, CPU) 크롤링
    if "orchestrator" in active_configs or not configs:
        app.send_task("orchestrator.tick", countdown=0)
    
    # 2분 뒤: 리테일 하드웨어 가격 (RAM, CPU, Retail GPU) 크롤링
    if "retail" in active_configs or not configs:
        app.send_task("retail.tick", countdown=120)
    
    # 4분 뒤: 금융 시장 데이터 (주식, 선물) 크롤링
    if "financial" in active_configs or not configs:
        app.send_task("market.tick", countdown=240)
    
    # 6분 뒤: 글로벌 뉴스 크롤링
    if "news_tier1_rss" in active_configs or not configs:
        app.send_task("news.tick", countdown=360)
    
    # 8분 뒤: 초고가 기업용 하드웨어(B2B) 장비 가격 크롤링
    if "enterprise" in active_configs or not configs:
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
