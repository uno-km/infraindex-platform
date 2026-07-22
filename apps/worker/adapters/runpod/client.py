import httpx
from typing import List, Dict, Any
from apps.worker.core.base_adapter import BaseProviderAdapter
from apps.worker.core.circuit_breaker import CircuitBreaker

class RunpodAdapter(BaseProviderAdapter):
    def __init__(self):
        super().__init__()
        self.client = httpx.AsyncClient(timeout=30.0)
        self.breaker = CircuitBreaker()
        
    @property
    def provider_slug(self) -> str:
        return "runpod"
        
    async def fetch_catalog(self) -> List[Dict[str, Any]]:
        if not self.breaker.allow_request():
            raise Exception("Circuit breaker is OPEN for Runpod")
            
        try:
            # GraphQL endpoint for Runpod catalog
            payload = {
                "query": "query { gpuTypes { id displayName memoryInGb securePrice communityPrice } }"
            }
            response = await self.client.post("https://api.runpod.io/graphql", json=payload)
            response.raise_for_status()
            self.breaker.record_success()
            data = response.json()
            return data.get("data", {}).get("gpuTypes", [])
        except Exception as e:
            self.breaker.record_failure()
            raise e
            
    async def fetch_prices(self) -> List[Dict[str, Any]]:
        # For Runpod, the pricing is included in the catalog endpoint above
        return await self.fetch_catalog()
            
    def normalize(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        from apps.worker.adapters.runpod.parser import RunpodParser
        return RunpodParser.parse(raw_data)
