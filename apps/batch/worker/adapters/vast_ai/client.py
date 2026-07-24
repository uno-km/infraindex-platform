import httpx
from typing import List, Dict, Any
from apps.batch.worker.core.base_adapter import BaseProviderAdapter
from apps.batch.worker.core.circuit_breaker import CircuitBreaker

class VastAiAdapter(BaseProviderAdapter):
    def __init__(self):
        super().__init__()
        self.client = httpx.AsyncClient(timeout=30.0)
        self.breaker = CircuitBreaker()
        
    @property
    def provider_slug(self) -> str:
        return "vast-ai"
        
    async def fetch_catalog(self) -> List[Dict[str, Any]]:
        # Vast.ai doesn't have a static catalog, it's all live offers.
        return []
        
    async def fetch_prices(self) -> List[Dict[str, Any]]:
        if not self.breaker.allow_request():
            raise Exception("Circuit breaker is OPEN for Vast.ai")
            
        try:
            # Example API endpoint for Vast.ai search
            response = await self.client.get("https://console.vast.ai/api/v0/bundles/")
            response.raise_for_status()
            self.breaker.record_success()
            data = response.json()
            return data.get("offers", [])
        except Exception as e:
            self.breaker.record_failure()
            raise e
            
    def normalize(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        from apps.batch.worker.adapters.vast_ai.parser import VastAiParser
        return VastAiParser.parse(raw_data)
