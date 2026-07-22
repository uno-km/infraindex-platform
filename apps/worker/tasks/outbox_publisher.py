"""
P2-002: Outbox Publisher — Celery Task

outbox_events 테이블에서 미처리(processed=False) 이벤트를 주기적으로 읽어
Redis Pub/Sub으로 전달하고 processed=True로 마킹.

- Celery Beat 스케줄: 30초마다 실행
- 배치 크기: 100개 (설정 가능)
- 전달 실패 시 재시도 3회 (backoff), 최종 실패 이벤트는 processed 유지 (재처리 가능)
- Redis Pub/Sub 미설정 시 로그만 기록 (graceful degradation)
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any

from celery import shared_task
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from apps.worker.core.config import settings

logger = logging.getLogger(__name__)

OUTBOX_BATCH_SIZE = 100


def _get_db_engine():
    db_url = settings.DATABASE_URL
    if not db_url:
        return None
    if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return create_async_engine(db_url, echo=False, future=True, pool_size=2, max_overflow=5)


async def _publish_batch() -> int:
    """
    미처리 Outbox 이벤트를 한 배치 처리.
    Returns: 처리된 이벤트 수
    """
    if not settings.USE_REAL_DB or not settings.DATABASE_URL:
        logger.debug("[OutboxPublisher] USE_REAL_DB=False — skipping.")
        return 0

    # 지연 임포트 (worker가 api 모델에 직접 의존하지 않도록)
    from apps.api.models.outbox import OutboxEvent

    engine = _get_db_engine()
    if not engine:
        return 0

    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    processed_count = 0

    try:
        # Redis 클라이언트 준비 (선택적)
        redis_client = None
        if settings.REDIS_URL:
            try:
                import redis.asyncio as aioredis
                redis_client = aioredis.from_url(settings.REDIS_URL)
                await redis_client.ping()
            except Exception as e:
                logger.warning(f"[OutboxPublisher] Redis 연결 실패 ({e}). 로그만 기록.")
                redis_client = None

        async with SessionLocal() as db:
            # 미처리 이벤트를 배치로 조회 (생성 순 오름차순)
            result = await db.execute(
                select(OutboxEvent)
                .where(OutboxEvent.processed == False)  # noqa: E712
                .order_by(OutboxEvent.created_at.asc())
                .limit(OUTBOX_BATCH_SIZE)
                .with_for_update(skip_locked=True)  # 분산 환경 동시 처리 방지
            )
            events = result.scalars().all()

            if not events:
                logger.debug("[OutboxPublisher] No pending events.")
                return 0

            logger.info(f"[OutboxPublisher] Processing {len(events)} pending events...")

            for event in events:
                try:
                    payload_str = json.dumps(event.payload, ensure_ascii=False)

                    # Redis Pub/Sub에 발행
                    if redis_client:
                        channel = f"events:{event.topic}"
                        message = json.dumps({
                            "event_id":   str(event.id),
                            "event_type": event.event_type,
                            "topic":      event.topic,
                            "payload":    event.payload,
                            "created_at": event.created_at.isoformat(),
                        })
                        await redis_client.publish(channel, message)
                        logger.info(
                            f"[OutboxPublisher] Published → channel={channel} "
                            f"event_type={event.event_type} id={event.id}"
                        )
                    else:
                        # Redis 없음: 이벤트 로그만 기록
                        logger.info(
                            f"[OutboxPublisher] Event (log-only): "
                            f"topic={event.topic} type={event.event_type} "
                            f"payload={payload_str[:200]}"
                        )

                    # 처리 완료 마킹
                    event.processed = True
                    event.processed_at = datetime.now(timezone.utc)
                    processed_count += 1

                except Exception as e:
                    logger.error(
                        f"[OutboxPublisher] Failed to process event {event.id}: {e}"
                    )
                    # 실패한 이벤트는 processed=False 유지 → 다음 배치에서 재시도

            await db.commit()

        if redis_client:
            await redis_client.aclose()

    except Exception as e:
        logger.error(f"[OutboxPublisher] Batch processing error: {e}", exc_info=True)
    finally:
        await engine.dispose()

    logger.info(f"[OutboxPublisher] Batch done: {processed_count} events published.")
    return processed_count


@shared_task(
    name="outbox.publish_pending",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def publish_pending_events() -> Any:
    """
    Celery Beat에 의해 30초마다 실행.
    처리되지 않은 Outbox 이벤트를 Redis Pub/Sub으로 전달.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        count = loop.run_until_complete(_publish_batch())
        return {"published": count}
    finally:
        loop.close()
