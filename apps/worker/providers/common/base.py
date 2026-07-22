from abc import ABC, abstractmethod
from typing import Any, Dict, List
import logging
from apps.worker.providers.common.http_client import StealthHttpClient

class BaseProviderCrawler(ABC):
    """
    Enterprise Abstract Factory Pattern for all Market Providers.
    Forces a strict contract for all data extraction modules.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.provider_slug}")
        self.http = StealthHttpClient()

    @property
    @abstractmethod
    def provider_slug(self) -> str:
        """Returns the unique identifier for the provider (e.g. 'vast-ai')"""
        pass

    @abstractmethod
    async def fetch_raw_data(self) -> Any:
        """Fetches raw data from the provider's API or Webpage."""
        pass

    @abstractmethod
    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        """Parses the raw structure into a flat list of instance dictionaries."""
        pass

    @abstractmethod
    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalizes the data into standard InfraIndex schemas 
        (e.g., standardizing GPU names, converting currencies to USD/hr).
        """
        pass

    async def execute_pipeline(self) -> List[Dict[str, Any]]:
        """Executes the full Extraction & Transformation pipeline."""
        self.logger.info(f"[{self.provider_slug}] Starting extraction pipeline...")
        raw = await self.fetch_raw_data()
        parsed = self.parse_instances(raw)
        normalized = self.normalize_pricing(parsed)
        self.logger.info(f"[{self.provider_slug}] Extracted {len(normalized)} normalized instances.")
        return normalized
