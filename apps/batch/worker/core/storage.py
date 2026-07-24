"""
스토리지 레이어 — PostgreSQL / JSON 파일 이중화.

주요 변경 사항:
  1. PostgresStorage 엔진 싱글턴:
     - 기존: save() 호출마다 create_async_engine() 생성 → 연결 폭발
     - 수정: 모듈 레벨 singleton으로 한 번만 생성
  2. Outbox 패턴 완성:
     - PriceHistory INSERT와 OutboxEvent INSERT를 동일 트랜잭션에서 실행
     - 한쪽만 커밋되는 dual-write 버그 방지
"""

import os
import json
from datetime import datetime, timezone
from typing import Any, List, Dict, Optional
from abc import ABC, abstractmethod
import logging

from apps.batch.worker.core.config import settings

logger = logging.getLogger(__name__)

# ── PostgreSQL 싱글턴 엔진 ────────────────────────────────────────────────
_pg_engine = None
_pg_session_factory = None


def _ensure_pg_engine():
    """
    모듈 레벨 싱글턴 엔진 + 세션 팩토리.
    첫 호출 시 생성, 이후 재사용.
    """
    global _pg_engine, _pg_session_factory
    if _pg_engine is not None:
        return _pg_engine, _pg_session_factory

    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

    db_url = settings.DATABASE_URL
    if not db_url:
        raise RuntimeError(
            "DATABASE_URL 환경변수가 설정되지 않았습니다. "
            "USE_REAL_DB=True 사용 시 DATABASE_URL 필수."
        )
    if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    _pg_engine = create_async_engine(
        db_url,
        echo=False,
        future=True,
        pool_size=3,           # worker는 소수 동시 실행
        max_overflow=5,
        pool_pre_ping=True,    # 스테일 커넥션 감지
        pool_recycle=1800,     # 30분마다 갱신
        connect_args={
            "server_settings": {
                "jit": "off",
                "statement_timeout": "15000",  # 15초 — 배치 INSERT용 여유
            }
        },
    )
    _pg_session_factory = async_sessionmaker(
        bind=_pg_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    logger.info(f"[PostgresStorage] Engine singleton created → {db_url.split('@')[-1]}")
    return _pg_engine, _pg_session_factory


class BaseStorage(ABC):
    @abstractmethod
    async def save(self, provider_slug: str, data: List[Dict[str, Any]]) -> None:
        pass


class JsonFileStorage(BaseStorage):
    """로컬 개발/테스트용 JSON 파일 저장소 (USE_REAL_DB=False)"""

    def __init__(self):
        os.makedirs(settings.LOCAL_STORAGE_DIR, exist_ok=True)

    async def save(self, provider_slug: str, data: List[Dict[str, Any]]) -> None:
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(settings.LOCAL_STORAGE_DIR, f"{provider_slug}_{date_str}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"[{provider_slug}] Saved {len(data)} records to {file_path}")


class PostgresStorage(BaseStorage):
    """
    실제 PostgreSQL 저장 구현.

    트랜잭션 보장:
      - PriceHistory INSERT + OutboxEvent INSERT를 동일 트랜잭션에서 실행.
      - 하나라도 실패하면 전체 롤백 → dual-write 버그 방지.
    """

    async def save(self, provider_slug: str, data: List[Dict[str, Any]]) -> None:
        if not data:
            logger.info(f"[{provider_slug}] No data to save.")
            return

        from apps.batch.services.gpu.models_history import GpuPriceHistory
        from shared.models.outbox import OutboxEvent

        _, SessionLocal = _ensure_pg_engine()

        now = datetime.now(timezone.utc)
        saved_count = 0
        error_count = 0

        async with SessionLocal() as session:
            async with session.begin():
                for item in data:
                    try:
                        gpu_model = item.get("gpu_model") or item.get("gpu_name") or "Unknown"
                        vram_gb_raw = item.get("vram_gb", 0)
                        price_raw = item.get("price_per_hour") or item.get("hourly_price") or 0.0

                        # ── GpuPriceHistory INSERT ────────────────────────────
                        record = GpuPriceHistory(
                            prv_id=provider_slug,
                            gpu_mdl=str(gpu_model)[:100],
                            vram_gb=float(vram_gb_raw) if vram_gb_raw else 0.0,
                            prc_ph=float(price_raw),
                            avl_st=str(item.get("availability_status", "unknown"))[:50],
                            ts=now,
                        )
                        session.add(record)

                        # ── OutboxEvent INSERT (동일 트랜잭션) ────────────
                        # Outbox Publisher가 이 이벤트를 Redis Pub/Sub으로 전달
                        outbox_event = OutboxEvent(
                            tpc_nm="price_updates",
                            evt_typ="price.collected",
                            payld_dat={
                                "provider_id": provider_slug,
                                "gpu_model": str(gpu_model)[:100],
                                "price_per_hour": float(price_raw),
                                "vram_gb": float(vram_gb_raw) if vram_gb_raw else 0.0,
                                "availability_status": str(item.get("availability_status", "unknown")),
                                "timestamp": now.isoformat(),
                            },
                        )
                        session.add(outbox_event)

                        saved_count += 1

                    except Exception as e:
                        logger.error(
                            f"[{provider_slug}] Failed to prepare record: {e} | data: {item}"
                        )
                        error_count += 1

        logger.info(
            f"[{provider_slug}] PostgreSQL 저장 완료: "
            f"{saved_count} rows inserted (PriceHistory + OutboxEvent), "
            f"{error_count} errors | timestamp={now.isoformat()}"
        )


def get_storage() -> BaseStorage:
    if settings.USE_REAL_DB:
        return PostgresStorage()
    return JsonFileStorage()


