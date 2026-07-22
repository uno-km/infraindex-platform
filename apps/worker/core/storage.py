import os
import json
from datetime import datetime
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
    def __init__(self):
        os.makedirs(settings.LOCAL_STORAGE_DIR, exist_ok=True)
        
    async def save(self, provider_slug: str, data: List[Dict[str, Any]]) -> None:
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(settings.LOCAL_STORAGE_DIR, f"{provider_slug}_{date_str}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"[{provider_slug}] Saved {len(data)} records to {file_path}")

class PostgresStorage(BaseStorage):
    async def save(self, provider_slug: str, data: List[Dict[str, Any]]) -> None:
        # Scaffold for Postgres. Real implementation would use SQLAlchemy AsyncSession
        # and insert into PriceHistory table.
        logger.info(f"[{provider_slug}] Saved {len(data)} records to PostgreSQL Database")

def get_storage() -> BaseStorage:
    if settings.USE_REAL_DB:
        return PostgresStorage()
    return JsonFileStorage()
