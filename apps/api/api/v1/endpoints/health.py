from typing import Any
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as redis
import os

from apps.api.core.database import get_db
from apps.api.core.config import settings

router = APIRouter()

@router.get("/")
async def health_check(response: Response, db: AsyncSession = Depends(get_db)) -> Any:
    """
    Dependency-Aware Health Check (Requirement 62).
    Verifies that Postgres and Redis are actually alive and reachable.
    """
    health_status = {
        "status": "healthy",
        "dependencies": {
            "database": "unknown",
            "redis": "unknown"
        }
    }
    
    # Check Database
    try:
        await db.execute(text("SELECT 1"))
        health_status["dependencies"]["database"] = "ok"
    except Exception as e:
        health_status["dependencies"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
        
    # Check Redis
    try:
        redis_client = redis.from_url(settings.CELERY_BROKER_URL)
        await redis_client.ping()
        await redis_client.close()
        health_status["dependencies"]["redis"] = "ok"
    except Exception as e:
        health_status["dependencies"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
        
    # Set proper HTTP status code
    if health_status["status"] == "unhealthy":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
    return health_status
