import os
import json
from datetime import datetime, timezone
from typing import Any, List, Dict
from abc import ABC, abstractmethod
import logging

from apps.worker.core.config import settings

logger = logging.getLogger(__name__)


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
    FIX-06 & FIX-07: 실제 PostgreSQL 저장 구현.

    수집된 정규화 데이터를 price_history 테이블에 INSERT.
    각 수집 실행마다 새 row를 추가하여 시계열 이력을 보존.
    동일한 가격이라도 다른 시각의 관측은 별도 row로 저장됨.
    """

    async def save(self, provider_slug: str, data: List[Dict[str, Any]]) -> None:
        if not data:
            logger.info(f"[{provider_slug}] No data to save.")
            return

        # 지연 임포트: worker가 항상 API 모델에 의존하지 않도록
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
        from apps.api.models.history import PriceHistory

        engine = create_async_engine(
            self._get_db_url(),
            echo=False,
            future=True,
            pool_size=5,
            max_overflow=10,
        )
        SessionLocal = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

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

                        record = PriceHistory(
                            provider_id=provider_slug,
                            gpu_model=str(gpu_model)[:100],
                            vram_gb=float(vram_gb_raw) if vram_gb_raw else 0.0,
                            price_per_hour=float(price_raw),
                            availability_status=str(item.get("availability_status", "unknown"))[:50],
                            timestamp=now,
                        )
                        session.add(record)
                        saved_count += 1
                    except Exception as e:
                        logger.error(f"[{provider_slug}] Failed to prepare record: {e} | data: {item}")
                        error_count += 1

        await engine.dispose()

        logger.info(
            f"[{provider_slug}] PostgreSQL 저장 완료: "
            f"{saved_count} rows inserted, {error_count} errors | timestamp={now.isoformat()}"
        )

    @staticmethod
    def _get_db_url() -> str:
        """DATABASE_URL 환경변수 우선, 없으면 개별 변수 조합"""
        url = settings.DATABASE_URL
        if url:
            # asyncpg 드라이버 보장
            if url.startswith("postgresql://") and "+asyncpg" not in url:
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url
        # Fallback: 개별 환경변수
        raise RuntimeError(
            "DATABASE_URL 환경변수가 설정되지 않았습니다. "
            "USE_REAL_DB=True 사용 시 DATABASE_URL 필수."
        )


def get_storage() -> BaseStorage:
    if settings.USE_REAL_DB:
        return PostgresStorage()
    return JsonFileStorage()
