import asyncio
import json
from typing import Any, AsyncGenerator
from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

from shared.config.settings import settings

router = APIRouter()

# SSE 연결당 최대 활성 시간 (초) — 무한 연결로 인한 리소스 고갈 방지
SSE_MAX_DURATION = 300  # 5분


async def _redis_event_generator(request: Request) -> AsyncGenerator[dict, None]:
    """
    Redis Pub/Sub 기반 SSE 이벤트 스트림.
    Outbox Publisher가 'events:*' 채널로 발행한 이벤트를 구독하여
    브라우저 클라이언트에 실시간 전송.

    DB 세션을 SSE 스트림 내부에서 유지하지 않음 (세션 누수 수정).
    연결 종료 시 Redis 구독 해제 + 연결 정리.
    """
    import redis.asyncio as aioredis

    redis_client = None
    pubsub = None
    elapsed = 0

    try:
        redis_client = aioredis.from_url(settings.REDIS_URL)
        pubsub = redis_client.pubsub()
        await pubsub.psubscribe("events:*")  # 모든 이벤트 토픽 구독

        # 연결 확인 핑
        yield {"event": "connected", "data": json.dumps({"status": "connected", "channel": "events:*"})}

        while True:
            # 클라이언트 연결 해제 감지
            if await request.is_disconnected():
                break

            # 최대 연결 시간 초과
            if elapsed >= SSE_MAX_DURATION:
                yield {"event": "timeout", "data": json.dumps({"message": "Stream timeout. Reconnect."})}
                break

            # Redis 메시지 비동기 수신 (100ms 타임아웃)
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=0.1)

            if message and message["type"] == "pmessage":
                try:
                    data = json.loads(message["data"])
                    yield {
                        "event": data.get("event_type", "price_update"),
                        "data": json.dumps(data),
                        "id": data.get("event_id", ""),
                    }
                except (json.JSONDecodeError, KeyError):
                    pass

            await asyncio.sleep(0.1)
            elapsed += 0.1

    except Exception as e:
        yield {"event": "error", "data": json.dumps({"message": str(e)})}

    finally:
        # 반드시 정리 (누수 방지)
        if pubsub:
            try:
                await pubsub.punsubscribe("events:*")
                await pubsub.aclose()
            except Exception:
                pass
        if redis_client:
            try:
                await redis_client.aclose()
            except Exception:
                pass


async def _fallback_event_generator(request: Request) -> AsyncGenerator[dict, None]:
    """
    Redis 미설정 시 폴백: DB 직접 폴링.
    독립적인 DB 세션을 each iteration마다 열고 닫음 (SSE 수명 동안 세션 유지 X).
    """
    from sqlalchemy import select
    from shared.models.outbox import OutboxEvent

    elapsed = 0
    seen_ids: set = set()

    yield {"event": "connected", "data": json.dumps({"status": "connected", "mode": "polling"})}

    while True:
        if await request.is_disconnected():
            break
        if elapsed >= SSE_MAX_DURATION:
            yield {"event": "timeout", "data": json.dumps({"message": "Stream timeout. Reconnect."})}
            break

        # 매 반복마다 독립 세션 사용 (누수 없음)
        try:
            from shared.db.session import AsyncSessionLocal as _SessionLocal
            async with _SessionLocal() as db:
                result = await db.execute(
                    select(OutboxEvent)
                    .where(OutboxEvent.processed == True)  # noqa
                    .order_by(OutboxEvent.processed_at.desc())
                    .limit(5)
                )
                events = result.scalars().all()

            for ev in events:
                eid = str(ev.id)
                if eid not in seen_ids:
                    seen_ids.add(eid)
                    yield {
                        "event": ev.event_type,
                        "data": json.dumps(ev.payload),
                        "id": eid,
                    }
        except Exception:
            pass

        await asyncio.sleep(2.0)
        elapsed += 2.0


@router.get("/prices")
async def stream_prices(request: Request) -> Any:
    """
    Real-time SSE (Server-Sent Events) Gateway for browser clients.
    Connect here to receive live price ticks.

    수정사항 (SSE 세션 누수 수정):
    - DB 세션을 SSE 스트림 내부에서 장기 유지하지 않음
    - Redis 설정 시: Redis Pub/Sub 구독 (Outbox Publisher 채널)
    - Redis 미설정 시: 독립 세션 폴링 폴백 (2초 간격)
    - 연결 해제 시 반드시 정리 (finally 블록)
    - 최대 5분 연결 후 재연결 유도
    """
    if settings.REDIS_URL:
        generator = _redis_event_generator(request)
    else:
        generator = _fallback_event_generator(request)

    return EventSourceResponse(generator)
