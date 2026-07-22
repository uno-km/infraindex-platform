"""
Redis 전역 싱글턴 ConnectionPool.

문제: 기존 코드는 health.py, stream.py 등에서 요청마다
     redis.asyncio.from_url()로 새 연결을 생성 → 연결 폭발 위험.

해결: 프로세스당 단 하나의 ConnectionPool을 유지.
     일반 요청용(cache) + Pub/Sub 전용 pool을 분리.

사용법:
    from apps.api.core.redis_client import get_redis, get_pubsub_redis

    async def my_endpoint(redis=Depends(get_redis)):
        await redis.set("key", "value", ex=CACHE_TTL_SHORT)
"""

import logging
from typing import AsyncGenerator, Optional

import redis.asyncio as aioredis
from redis.asyncio import ConnectionPool

from apps.api.core.config import settings

logger = logging.getLogger(__name__)

# ── TTL 상수 (초) ────────────────────────────────────────────────────────
CACHE_TTL_SHORT = 60        # 1분 — 실시간성 높은 데이터 (가격, health)
CACHE_TTL_MEDIUM = 600      # 10분 — 검색 결과, 집계
CACHE_TTL_LONG = 3600       # 1시간 — 공급자 목록, GPU 카탈로그
CACHE_TTL_DAY = 86400       # 24시간 — 이력 요약, 리포트

# ── 전역 Pool 인스턴스 ────────────────────────────────────────────────────
_cache_pool: Optional[ConnectionPool] = None
_pubsub_pool: Optional[ConnectionPool] = None


def _build_pool(max_connections: int = 50) -> ConnectionPool:
    """Redis ConnectionPool 생성."""
    return aioredis.BlockingConnectionPool.from_url(
        settings.REDIS_URL,
        max_connections=max_connections,
        timeout=5,          # 풀에서 커넥션 획득 최대 대기 (초)
        socket_connect_timeout=3,
        socket_timeout=3,
        decode_responses=True,
        health_check_interval=30,  # 주기적 ping으로 스테일 연결 감지
    )


def init_redis_pool() -> None:
    """
    FastAPI 앱 startup 시 호출.
    전역 pool을 초기화한다.
    """
    global _cache_pool, _pubsub_pool
    max_conn = getattr(settings, "REDIS_MAX_CONNECTIONS", 50)
    _cache_pool = _build_pool(max_connections=max_conn)
    _pubsub_pool = _build_pool(max_connections=10)  # Pub/Sub은 소수 연결로 충분
    logger.info(
        f"[Redis] Pools initialized — cache(max={max_conn}), pubsub(max=10) "
        f"→ {settings.REDIS_URL.split('@')[-1]}"
    )


async def close_redis_pool() -> None:
    """
    FastAPI 앱 shutdown 시 호출.
    모든 연결을 graceful close.
    """
    global _cache_pool, _pubsub_pool
    if _cache_pool:
        await _cache_pool.aclose()
        _cache_pool = None
        logger.info("[Redis] Cache pool closed.")
    if _pubsub_pool:
        await _pubsub_pool.aclose()
        _pubsub_pool = None
        logger.info("[Redis] PubSub pool closed.")


def _get_cache_pool() -> ConnectionPool:
    if _cache_pool is None:
        # startup이 안 됐을 경우 fallback 초기화 (개발 편의)
        logger.warning("[Redis] Pool was not initialized — lazy init. Call init_redis_pool() at startup.")
        init_redis_pool()
    return _cache_pool


def _get_pubsub_pool() -> ConnectionPool:
    if _pubsub_pool is None:
        init_redis_pool()
    return _pubsub_pool


# ── FastAPI Depends 의존성 ───────────────────────────────────────────────

async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """
    일반 캐시/pub 요청용 Redis 클라이언트 의존성.

    사용:
        async def endpoint(redis: aioredis.Redis = Depends(get_redis)):
            await redis.get("key")
    """
    client = aioredis.Redis(connection_pool=_get_cache_pool())
    try:
        yield client
    finally:
        # pool 기반이므로 close()는 커넥션을 pool로 반환할 뿐
        await client.aclose()


async def get_pubsub_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """
    Pub/Sub 전용 Redis 클라이언트 의존성.
    일반 cache pool과 분리하여 pub/sub이 cache를 starve하지 않음.
    """
    client = aioredis.Redis(connection_pool=_get_pubsub_pool())
    try:
        yield client
    finally:
        await client.aclose()


def get_redis_client() -> aioredis.Redis:
    """
    비-async 컨텍스트나 worker에서 직접 사용하는 동기 factory.
    반환된 클라이언트는 사용 후 반드시 aclose()를 호출해야 함.
    """
    return aioredis.Redis(connection_pool=_get_cache_pool())
