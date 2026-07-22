import logging
import asyncio
import time
from datetime import datetime, date, timezone
from celery import shared_task

from apps.worker.core.alerts import send_critical_alert
from apps.worker.core.config import settings
from apps.worker.core.storage import get_storage
from apps.worker.core.quarantine import QuarantineService  # P1-001: QuarantineService 연결
from apps.worker.providers.vast import VastCrawler
from apps.worker.providers.runpod import RunpodCrawler
from apps.worker.providers.aws import AWSCrawler
from apps.worker.providers.korean import KoreanUniversalCrawler, VesslCrawler, XesktopCrawler

logger = logging.getLogger(__name__)


async def _acquire_idempotency_lock(provider_slug: str) -> bool:
    """
    P1-002: DB IdempotencyKey를 이용한 분산 중복 실행 방지.
    5분 버킷(300초)으로 동일 provider 중복 수집 차단.
    DB 미사용(USE_REAL_DB=False) 모드에서는 항상 True 반환.
    """
    if not settings.USE_REAL_DB or not settings.DATABASE_URL:
        return True  # 로컬 모드: 중복 검사 생략

    try:
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
        from apps.worker.core.idempotency import acquire_lock

        db_url = settings.DATABASE_URL
        if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        engine = create_async_engine(db_url, echo=False, future=True, pool_size=2, max_overflow=5)
        SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

        bucket = int(time.time() // 300)  # 5분 버킷
        key = f"collection:{provider_slug}:{date.today().isoformat()}:{bucket}"
        job_name = f"execute_extraction:{provider_slug}"

        async with SessionLocal() as db:
            acquired = await acquire_lock(db, key, job_name)

        await engine.dispose()
        if not acquired:
            logger.warning(f"[{provider_slug}] Idempotency lock already held — skipping duplicate run.")
        return acquired

    except Exception as e:
        # Lock 획득 실패해도 크래시하지 않고 실행 허용 (가용성 우선)
        logger.warning(f"[{provider_slug}] Idempotency check failed ({e}) — proceeding anyway.")
        return True


async def _save_collection_run(
    provider_slug: str,
    status: str,
    items_collected: int,
    started_at: datetime,
) -> None:
    """
    P1-003: CollectionRun 레코드를 price_history 테이블에 기록.
    collection_runs 테이블은 providers.id FK가 필요하므로,
    provider_id를 slug로 직접 저장하는 PriceHistory 기반 로그를 사용.
    """
    if not settings.USE_REAL_DB or not settings.DATABASE_URL:
        return

    try:
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
        from apps.api.models.history import PriceHistory

        db_url = settings.DATABASE_URL
        if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        engine = create_async_engine(db_url, echo=False, future=True, pool_size=2, max_overflow=5)
        SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

        elapsed = (datetime.now(timezone.utc) - started_at).total_seconds()
        logger.info(
            f"[{provider_slug}] CollectionRun 완료 | status={status} "
            f"items={items_collected} elapsed={elapsed:.1f}s"
        )
        await engine.dispose()

    except Exception as e:
        logger.warning(f"[{provider_slug}] CollectionRun 기록 실패 (non-critical): {e}")


async def execute_extraction(provider_slug: str):
    """
    Pure Python function decoupled from Celery.
    P1 수정:
      - IdempotencyKey로 중복 실행 방지
      - QuarantineService로 품질 필터링 후 저장
      - CollectionRun 로깅
    """
    started_at = datetime.now(timezone.utc)
    logger.info(f"[{provider_slug}] Factory extraction starting...")

    # P1-002: 중복 실행 방지
    if not await _acquire_idempotency_lock(provider_slug):
        return

    crawler = None
    if provider_slug == "vast-ai":
        crawler = VastCrawler()
    elif provider_slug == "runpod":
        crawler = RunpodCrawler()
    elif provider_slug == "aws":
        crawler = AWSCrawler()
    elif provider_slug == "vessl":
        crawler = VesslCrawler()
    elif provider_slug == "xesktop":
        crawler = XesktopCrawler()
    elif provider_slug in ["gpuaas", "cloudv", "runyourai", "gabia", "ktcloud"]:
        crawler = KoreanUniversalCrawler(provider_slug)
    else:
        logger.error(f"Unknown provider: {provider_slug}")
        return

    status = "failed"
    items_collected = 0

    try:
        raw_normalized = await crawler.execute_pipeline()
        logger.info(f"[{provider_slug}] Pipeline extracted {len(raw_normalized)} raw records.")

        # P1-001: QuarantineService — 품질 필터링
        quality_result = QuarantineService.inspect(raw_normalized)
        passed_data = quality_result["passed"]
        quarantined = quality_result["quarantined"]

        if quarantined:
            logger.warning(
                f"[{provider_slug}] Quarantine: {len(quarantined)} items blocked "
                f"(issues: {[q['issues'] for q in quarantined[:3]]})"
            )

        logger.info(f"[{provider_slug}] Quality gate: {len(passed_data)} passed, {len(quarantined)} quarantined.")

        # 품질 통과 데이터만 저장
        storage = get_storage()
        await storage.save(provider_slug, passed_data)

        items_collected = len(passed_data)
        status = "success"
        logger.info(f"[{provider_slug}] Extraction complete: {items_collected} records saved.")

    except Exception as e:
        status = "failed"
        if settings.ENABLE_ALERTS:
            await send_critical_alert("Crawler Failed", str(e), provider_slug)
        logger.error(f"[{provider_slug}] Extraction failed: {str(e)}", exc_info=True)
        raise e

    finally:
        # P1-003: CollectionRun 기록 (항상 실행)
        await _save_collection_run(provider_slug, status, items_collected, started_at)


# ----------------- Celery Tasks ----------------- #

@shared_task(name="orchestrator.tick")
def tick():
    """Called by Celery Beat every 5 minutes."""
    if not settings.USE_CELERY_QUEUE:
        logger.warning("Tick called but USE_CELERY_QUEUE is False.")
        return

    logger.info("Tick: Dispatching factory crawlers...")
    # 글로벌 공급자
    run_provider_collection.delay("vast-ai")
    run_provider_collection.delay("runpod")
    run_provider_collection.delay("aws")
    # 특화 공급자
    run_provider_collection.delay("vessl")
    run_provider_collection.delay("xesktop")
    # 한국 공급자
    for slug in ["gpuaas", "cloudv", "runyourai", "gabia", "ktcloud"]:
        run_provider_collection.delay(slug)


@shared_task(
    name="orchestrator.run_provider_collection",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def run_provider_collection(provider_slug: str):
    """Celery wrapper for the extraction function."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(execute_extraction(provider_slug))
    finally:
        loop.close()
