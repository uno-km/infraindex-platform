import uuid
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware

import shared.models  # Preload models to fix circular imports
from apps.server.api.v1.api import api_router
from apps.server.api.v1.endpoints import admin
from shared.config.settings import settings
from apps.server.core.limiter import limiter

logger = logging.getLogger(__name__)


# ── Lifecycle (startup / shutdown) ───────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan: startup → 앱 실행 → shutdown.
    startup: Redis pool + DB engine 초기화
    shutdown: 모든 연결 graceful close
    """
    # STARTUP ──────────────────────────────────
    logger.info("[Startup] Initializing infrastructure...")

    # 1. Redis 전역 Pool 초기화
    try:
        from apps.server.core.redis_client import init_redis_pool
        init_redis_pool()
    except Exception as e:
        logger.warning(f"[Startup] Redis pool init failed: {e}. Continuing without Redis.")

    # 2. DB Engine 초기화 (pool_pre_ping으로 연결 검증)
    try:
        from shared.db.session import init_db_engine
        init_db_engine()
    except Exception as e:
        logger.warning(f"[Startup] DB engine init failed: {e}. Check DATABASE_URL.")

    # 3. FastAPI Cache 초기화 (Redis Backend)
    try:
        from fastapi_cache import FastAPICache
        from fastapi_cache.backends.redis import RedisBackend
        from redis import asyncio as aioredis
        redis_client = aioredis.from_url(settings.REDIS_URL)
        FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
        logger.info("[Startup] FastAPI Cache initialized.")
    except Exception as e:
        logger.warning(f"[Startup] FastAPI Cache init failed: {e}")
        print(f"[Startup] FastAPI Cache init failed: {e}")

    logger.info("[Startup] Infrastructure ready.")
    yield

    # SHUTDOWN ─────────────────────────────────
    logger.info("[Shutdown] Closing infrastructure connections...")

    try:
        from apps.server.core.redis_client import close_redis_pool
        await close_redis_pool()
    except Exception as e:
        logger.warning(f"[Shutdown] Redis pool close error: {e}")

    try:
        from shared.db.session import dispose_db_engine
        await dispose_db_engine()
    except Exception as e:
        logger.warning(f"[Shutdown] DB engine dispose error: {e}")

    logger.info("[Shutdown] Graceful shutdown complete.")


# ── App 생성 ─────────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


# ── Middleware Stack (LIFO 순서로 적용됨) ────────────────────────────────

# 1. Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) # type: ignore


# 2. X-Request-ID — 분산 추적 / 로그 correlation
class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    각 요청에 고유한 X-Request-ID를 부여.
    클라이언트가 헤더를 보내면 그대로 사용, 없으면 UUID 생성.
    응답 헤더에도 포함하여 클라이언트가 추적 가능.
    """
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

app.add_middleware(RequestIDMiddleware)


# 3. Security Headers — 웹 배포 필수 보안 헤더
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Content-Security-Policy:
      - default-src 'self': 기본적으로 동일 출처만 허용
      - script-src 'self' 'unsafe-inline': Next.js SSR 인라인 스크립트 허용
      - img-src *: 외부 이미지 (GPU 제조사 로고 등) 허용
    HSTS: 1년간 HTTPS 강제 (includeSubDomains 포함)
    """
    CSP = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https:; "
        "frame-ancestors 'none';"
    )

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # 기존 헤더 유지 + 추가
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )
        response.headers["Content-Security-Policy"] = self.CSP
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=()"
        )
        if "server" in response.headers:
            del response.headers["server"]
        if "x-powered-by" in response.headers:
            del response.headers["x-powered-by"]
        return response

app.add_middleware(SecurityHeadersMiddleware)


# 4. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)


# 5. TrustedHostMiddleware — Host 헤더 스푸핑 방지
# TRUSTED_HOSTS가 빈 리스트면 미들웨어 비활성화 (로컬 개발 편의)
if settings.TRUSTED_HOSTS:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.TRUSTED_HOSTS,
    )


# ── Observability ─────────────────────────────────────────────────────────
Instrumentator().instrument(app).expose(app)


# -----------------------------------------------------------------------------
# Static Files
# -----------------------------------------------------------------------------
import os
from fastapi.staticfiles import StaticFiles

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "storage")
os.makedirs(os.path.join(STORAGE_DIR, "reports"), exist_ok=True)
app.mount("/storage", StaticFiles(directory=STORAGE_DIR), name="storage")


# -----------------------------------------------------------------------------
# Routers
# -----------------------------------------------------------------------------
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the InfraIndex API"}

