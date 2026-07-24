from typing import Any
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as aioredis

from shared.db.session import get_db
from shared.config.settings import settings
from apps.server.core.redis_client import get_redis

router = APIRouter()


@router.get("/")
async def health_check(
    response: Response,
    db: AsyncSession = Depends(get_db),
    redis_client: aioredis.Redis = Depends(get_redis),
) -> Any:
    """
    Dependency-Aware Health Check.
    - DB: AsyncSession ping (SELECT 1)
    - Redis: pool에서 획득한 클라이언트로 ping (새 연결 생성 X)
    Returns HTTP 200 if healthy, HTTP 503 if any dependency is down.
    """
    health_status = {
        "status": "healthy",
        "dependencies": {
            "database": "unknown",
            "redis": "unknown",
        }
    }

    # Check Database
    try:
        if db is None:
            health_status["dependencies"]["database"] = "disabled (USE_REAL_DB=False)"
        else:
            await db.execute(text("SELECT 1"))
            health_status["dependencies"]["database"] = "ok"
    except Exception as e:
        health_status["dependencies"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check Redis (전역 pool에서 획득한 클라이언트 사용)
    try:
        await redis_client.ping()
        health_status["dependencies"]["redis"] = "ok"
    except Exception as e:
        health_status["dependencies"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"

    # Set proper HTTP status code
    if health_status["status"] == "unhealthy":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return health_status
