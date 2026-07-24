import logging
import asyncio
import time
from datetime import datetime, date, timezone
from celery import shared_task

from apps.worker.core.alerts import send_critical_alert
from apps.worker.core.config import settings
from apps.worker.core.storage import get_storage
from apps.worker.core.quarantine import QuarantineService  # P1-001: QuarantineService 연결
from apps.services.gpu.crawler_vast import VastCrawler
from apps.services.gpu.crawler_runpod import RunpodCrawler
from apps.services.gpu.crawler_aws import AWSCrawler
from apps.services.gpu.crawler_korean import KoreanUniversalCrawler, VesslCrawler, XesktopCrawler

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
from celery import chain
from sqlalchemy import select
from apps.worker.core.schedule_manager import schedule_manager

@shared_task(name="orchestrator.refresh_schedules")
def refresh_schedules():
    """Admin API에서 호출 시 메모리에 적재된 스케줄을 갱신합니다."""
    logger.info("Refreshing batch schedules in memory...")
    schedule_manager.load_sync()
    logger.info(f"Schedules refreshed: {list(schedule_manager.get_schedules().keys())}")

@shared_task(name="orchestrator.tick")
def tick():
    """Called by Celery Beat every 1 minute."""
    if not settings.USE_CELERY_QUEUE:
        logger.warning("Tick called but USE_CELERY_QUEUE is False.")
        return

    # 워커 시작 후 최초 호출이거나, 아직 로드가 안 된 경우 로드
    if not schedule_manager._is_loaded:
        schedule_manager.load_sync()

    schedules = schedule_manager.get_schedules()
    for bat_id, sched in schedules.items():
        if schedule_manager.is_time_to_run(bat_id):
            logger.info(f"Tick: 배치가 실행 조건에 맞습니다. Dispatching {bat_id}...")
            run_batch_chain.delay(bat_id)

async def _get_batch_details(bat_id: str):
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
        from apps.api.models.batch_schedule import SysBatSchDtl
        
        db_url = settings.DATABASE_URL
        if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        engine = create_async_engine(db_url, echo=False, future=True, pool_size=2, max_overflow=5)
        SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

        async with SessionLocal() as session:
            stmt = select(SysBatSchDtl).where(
                SysBatSchDtl.bat_id == bat_id,
                SysBatSchDtl.use_yn == "Y"
            ).order_by(SysBatSchDtl.run_ord)
            
            result = await session.execute(stmt)
            dtls = result.scalars().all()
            
            # extract job details
            jobs = [{"bat_id": dtl.bat_id, "job_id": dtl.job_id, "slug": dtl.ref_val_1} for dtl in dtls if dtl.ref_val_1]
            
        await engine.dispose()
        return jobs
    except Exception as e:
        logger.error(f"Failed to fetch DTLs for {bat_id}: {e}")
        return []

@shared_task(name="orchestrator.run_batch_chain")
def run_batch_chain(bat_id: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        jobs = loop.run_until_complete(_get_batch_details(bat_id))
    finally:
        loop.close()
        
    if not jobs:
        logger.warning(f"No DTLs found for {bat_id} or USE_YN is not 'Y'.")
        return
        
    logger.info(f"Constructing sequential chain for {bat_id}: {[j['slug'] for j in jobs]}")
    
    # 순차 실행을 위해 chain 구성 (si = immutable signature, 결과를 다음 태스크에 넘기지 않음)
    tasks = [run_provider_collection.si(j['bat_id'], j['job_id'], j['slug']) for j in jobs]
    workflow = chain(*tasks)
    workflow.apply_async()

async def _insert_history(bat_id: str, job_id: str, start_dt, end_dt, status: str, err_msg: str = None):
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
        from apps.api.models.batch_schedule import SysBatSchHist, SysBatSchDtl
        
        db_url = settings.DATABASE_URL
        if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        engine = create_async_engine(db_url, echo=False, future=True)
        SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

        async with SessionLocal() as session:
            # 1. Insert History
            hist = SysBatSchHist(
                bat_id=bat_id,
                job_id=job_id,
                start_dt=start_dt,
                end_dt=end_dt,
                status=status,
                err_msg=err_msg
            )
            session.add(hist)
            
            # 2. Update DTL LAST_RUN_DT
            from sqlalchemy import update
            stmt = update(SysBatSchDtl).where(
                SysBatSchDtl.bat_id == bat_id,
                SysBatSchDtl.job_id == job_id
            ).values(last_run_dt=end_dt)
            if err_msg:
                # err_msg 컬럼이 모델에 정의되어 있는지 확인 후 기록
                stmt = stmt.values(err_msg=err_msg[:500])
            
            await session.execute(stmt)
            await session.commit()
            
        await engine.dispose()
    except Exception as e:
        logger.error(f"Failed to insert history for {bat_id}/{job_id}: {e}")

async def _update_dtl_error(provider_slug: str, error_msg: str):
    try:
        from sqlalchemy import update
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
        from apps.api.models.batch_schedule import SysBatSchDtl
        
        db_url = settings.DATABASE_URL
        if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        engine = create_async_engine(db_url, echo=False, future=True)
        SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

        async with SessionLocal() as session:
            stmt = update(SysBatSchDtl).where(SysBatSchDtl.ref_val_1 == provider_slug).values(
                rmk=error_msg[:500]
            )
            await session.execute(stmt)
            await session.commit()
            
        await engine.dispose()
    except Exception as e:
        logger.error(f"Failed to update DTL error for {provider_slug}: {e}")

@shared_task(
    name="orchestrator.run_provider_collection",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def run_provider_collection(bat_id: str, job_id: str, provider_slug: str):
    """Celery wrapper for the extraction function with history logging."""
    import traceback
    from datetime import datetime, timezone
    
    start_dt = datetime.now(timezone.utc).replace(tzinfo=None)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(execute_extraction(provider_slug))
        end_dt = datetime.now(timezone.utc).replace(tzinfo=None)
        loop.run_until_complete(_insert_history(bat_id, job_id, start_dt, end_dt, "SUCCESS"))
    except Exception as e:
        end_dt = datetime.now(timezone.utc).replace(tzinfo=None)
        err_trace = traceback.format_exc()
        loop.run_until_complete(_insert_history(bat_id, job_id, start_dt, end_dt, "FAIL", err_trace))
        raise e
    finally:
        loop.close()
