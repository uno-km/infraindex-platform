"""
DB 연결 풀 — 프로덕션 튜닝 적용.

pool_pre_ping   : 스테일 커넥션 자동 감지 (DB 재시작 후 오류 방지)
pool_recycle    : 30분마다 커넥션 강제 갱신 (PgBouncer/Render 호환)
pool_size       : 환경변수 DB_POOL_SIZE (기본 5 — Render starter 적합)
max_overflow    : 환경변수 DB_MAX_OVERFLOW (기본 10)
pool_timeout    : 30초 — 풀 획득 타임아웃
connect_args    : asyncpg statement_timeout 10초
"""

import logging
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from shared.config.settings import settings

logger = logging.getLogger(__name__)

engine: Optional[AsyncEngine] = None
AsyncSessionLocal: Optional[async_sessionmaker] = None


def _build_engine() -> AsyncEngine:
    return create_async_engine(
        settings.async_database_uri,
        echo=False,
        future=True,
        # ── Pool 튜닝 ────────────────────────────────────────
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_pre_ping=True,          # 스테일 커넥션 자동 감지
        pool_recycle=settings.DB_POOL_RECYCLE,  # 30분마다 갱신
        pool_timeout=30,             # 풀에서 커넥션 획득 최대 대기
        # ── asyncpg 드라이버 설정 ────────────────────────────
        connect_args={
            "server_settings": {
                "jit": "off",            # 단순 OLTP 쿼리 JIT 불필요
                "statement_timeout": "10000",  # 10초 쿼리 타임아웃 (ms)
                "lock_timeout": "5000",        # 5초 락 타임아웃
            },
        },
    )


def _build_session_factory(eng: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(
        bind=eng,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


def init_db_engine() -> None:
    """
    FastAPI startup 시 호출.
    USE_REAL_DB=True인 경우에만 엔진을 생성.
    """
    global engine, AsyncSessionLocal
    if not settings.USE_REAL_DB:
        logger.info("[DB] USE_REAL_DB=False — DB engine 초기화 생략.")
        return
    engine = _build_engine()
    AsyncSessionLocal = _build_session_factory(engine)
    logger.info(
        f"[DB] Engine initialized — pool_size={settings.DB_POOL_SIZE}, "
        f"max_overflow={settings.DB_MAX_OVERFLOW}, "
        f"pool_recycle={settings.DB_POOL_RECYCLE}s"
    )


async def dispose_db_engine() -> None:
    """FastAPI shutdown 시 호출. 모든 DB 커넥션 graceful close."""
    global engine
    if engine is not None:
        await engine.dispose()
        engine = None
        logger.info("[DB] Engine disposed.")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI 의존성 주입용 DB 세션 generator.
    USE_REAL_DB=False이면 None을 yield (개발/테스트 모드).
    """
    if not settings.USE_REAL_DB or AsyncSessionLocal is None:
        yield None
        return

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ── 하위 호환 — 기존 코드에서 import 중인 legacy 이름 ──────────────────
# startup lifecycle 적용 전까지 engine/AsyncSessionLocal을 즉시 초기화
if settings.USE_REAL_DB:
    try:
        engine = _build_engine()
        AsyncSessionLocal = _build_session_factory(engine)
    except Exception as _e:
        logger.warning(f"[DB] Eager engine init failed: {_e}. Will retry at startup.")

