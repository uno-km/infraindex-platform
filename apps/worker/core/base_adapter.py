from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseProviderAdapter(ABC):
    def __init__(self):
        pass
        
    @property
    @abstractmethod
    def provider_slug(self) -> str:
        pass
        
    @abstractmethod
    async def fetch_catalog(self) -> List[Dict[str, Any]]:
        """Fetch base catalog of instances"""
        pass
        
    @abstractmethod
    async def fetch_prices(self) -> List[Dict[str, Any]]:
        """Fetch pricing for instances"""
        pass
        
    @abstractmethod
    def normalize(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize raw data to canonical schema"""
        pass
        
    async def run_collection(self):
        """Standard collection run"""
        catalog = await self.fetch_catalog()
        prices = await self.fetch_prices()
        normalized = self.normalize(prices)
        return normalized
