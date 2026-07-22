import json
import os
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseStorage(ABC):
    @abstractmethod
    async def save(self, provider_slug: str, data: List[Dict[str, Any]]) -> None:
        pass

class JsonFileStorage(BaseStorage):
    """
    Saves scraped data locally to a JSON file.
    Ideal for serverless/cron setups with zero DB costs.
    """
    def __init__(self, output_dir: str = "data"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    async def save(self, provider_slug: str, data: List[Dict[str, Any]]) -> None:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        file_path = os.path.join(self.output_dir, f"{provider_slug}_{date_str}.json")
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"[{provider_slug}] Successfully saved {len(data)} records to {file_path}")
        except Exception as e:
            logger.error(f"[{provider_slug}] Failed to save to JSON: {e}")
            raise e

class PostgresStorage(BaseStorage):
    """
    Saves scraped data to PostgreSQL via SQLAlchemy.
    Ideal for the Enterprise SaaS tier.
    """
    async def save(self, provider_slug: str, data: List[Dict[str, Any]]) -> None:
        logger.info(f"[{provider_slug}] (Mock) Saving {len(data)} records to PostgreSQL...")
        # TODO: Implement actual SQLAlchemy session and bulk insert here
        pass

def get_storage_backend(use_real_db: bool) -> BaseStorage:
    if use_real_db:
        return PostgresStorage()
    return JsonFileStorage()
