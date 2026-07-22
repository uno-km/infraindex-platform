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
    error_message: str | None = None,
) -> None:
    """
    CollectionRun 레코드를 collection_runs 테이블에 실제 INSERT.
    provider_id는 slug(문자열) 기반 — providers FK 없이도 기록 가능.
    """
    if not settings.USE_REAL_DB or not settings.DATABASE_URL:
        # 로컬 모드: 로그만 기록
        elapsed = (datetime.now(timezone.utc) - started_at).total_seconds()
        logger.info(
            f"[{provider_slug}] CollectionRun (local) | status={status} "
            f"items={items_collected} elapsed={elapsed:.1f}s"
        )
        return

    try:
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
        from apps.api.models.quality import CollectionRun

        db_url = settings.DATABASE_URL
        if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        engine = create_async_engine(db_url, echo=False, future=True, pool_size=2, max_overflow=3)
        SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

        completed_at = datetime.now(timezone.utc)
        elapsed = (completed_at - started_at).total_seconds()

        run = CollectionRun(
            provider_id=provider_slug,
            started_at=started_at,
            completed_at=completed_at,
            status=status,
            items_collected=items_collected,
            error_message=error_message,
        )

        async with SessionLocal() as db:
            async with db.begin():
                db.add(run)

        await engine.dispose()
        logger.info(
            f"[{provider_slug}] CollectionRun INSERT 완료 | status={status} "
            f"items={items_collected} elapsed={elapsed:.1f}s"
        )

    except Exception as e:
        logger.warning(f"[{provider_slug}] CollectionRun 기록 실패 (non-critical): {e}")


async def _save_quarantine_issues(
    provider_slug: str,
    quarantined: list,
    run_id: str | None = None,
) -> None:
    """
    DataQualityIssue 배치 INSERT.
    quarantined 아이템마다 issue_type, severity, description, raw_data_snapshot을 기록.
    """
    if not quarantined:
        return
    if not settings.USE_REAL_DB or not settings.DATABASE_URL:
        return

    try:
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
        from apps.api.models.quality import DataQualityIssue
        import json

        db_url = settings.DATABASE_URL
        if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        engine = create_async_engine(db_url, echo=False, future=True, pool_size=2, max_overflow=3)
        SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

        issues_to_insert = []
        for q in quarantined:
            raw_data = q.get("data", {})
            issue_types = q.get("issues", ["unknown_issue"])
            description = f"[{provider_slug}] Quarantined: {', '.join(issue_types)}"
            try:
                raw_snapshot = json.dumps(raw_data, ensure_ascii=False)[:2000]
            except Exception:
                raw_snapshot = str(raw_data)[:2000]

            for issue_type in issue_types:
                issues_to_insert.append(DataQualityIssue(
                    run_id=run_id,
                    issue_type=issue_type,
                    severity="quarantine",
                    description=description,
                    raw_data_snapshot=raw_snapshot,
                ))

        async with SessionLocal() as db:
            async with db.begin():
                db.add_all(issues_to_insert)

        await engine.dispose()
        logger.info(f"[{provider_slug}] DataQualityIssue INSERT: {len(issues_to_insert)} rows")

    except Exception as e:
        logger.warning(f"[{provider_slug}] DataQualityIssue 기록 실패 (non-critical): {e}")


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
    elif provider_slug in ["gpuaas", "cloudv", "runyourai", "gabia", "ktcloud", "sugarcube", "appleplaza", "ncloud", "rebellion"]:
        crawler = KoreanUniversalCrawler(provider_slug)
    else:
        logger.error(f"Unknown provider: {provider_slug}")
        return

    status = "failed"
    items_collected = 0

    last_error: str | None = None

    try:
        raw_normalized = await crawler.execute_pipeline()
        logger.info(f"[{provider_slug}] Pipeline extracted {len(raw_normalized)} raw records.")

        # QuarantineService — 품질 필터링
        quality_result = QuarantineService.inspect(raw_normalized)
        passed_data = quality_result["passed"]
        quarantined = quality_result["quarantined"]

        if quarantined:
            logger.warning(
                f"[{provider_slug}] Quarantine: {len(quarantined)} items blocked "
                f"(issues: {[q['issues'] for q in quarantined[:3]]})"
            )

        logger.info(f"[{provider_slug}] Quality gate: {len(passed_data)} passed, {len(quarantined)} quarantined.")

        # 품질 통과 데이터만 저장 (PriceHistory + OutboxEvent 동일 트랜잭션)
        storage = get_storage()
        await storage.save(provider_slug, passed_data)

        # DataQualityIssue 배치 INSERT (quarantine 아이템 기록)
        if quarantined:
            await _save_quarantine_issues(provider_slug, quarantined)

        items_collected = len(passed_data)
        status = "success"
        logger.info(f"[{provider_slug}] Extraction complete: {items_collected} records saved.")

    except Exception as e:
        status = "failed"
        last_error = str(e)
        if settings.ENABLE_ALERTS:
            await send_critical_alert("Crawler Failed", str(e), provider_slug)
        logger.error(f"[{provider_slug}] Extraction failed: {str(e)}", exc_info=True)
        raise e

    finally:
        # CollectionRun 기록 (항상 실행 — 성공/실패 모두)
        await _save_collection_run(
            provider_slug, status, items_collected, started_at,
            error_message=last_error
        )


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
    for slug in ["gpuaas", "cloudv", "runyourai", "gabia", "ktcloud", "sugarcube", "appleplaza", "ncloud", "rebellion"]:
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
