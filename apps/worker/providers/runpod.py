from typing import Any, Dict, List
from apps.worker.providers.common.base import BaseProviderCrawler

class RunpodCrawler(BaseProviderCrawler):
    @property
    def provider_slug(self) -> str:
        return "runpod"

    async def fetch_raw_data(self) -> Any:
        client = await self.http.get_client()
        payload = {"query": "query { gpuTypes { id displayName memoryInGb securePrice communityPrice } }"}
        response = await client.post("https://api.runpod.io/graphql", json=payload)
        return response.json() if response.status_code == 200 else {}

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        return raw_data.get("data", {}).get("gpuTypes", [])

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for instance in parsed_data:
            normalized.append({
                "gpu_model": instance.get("id"),
                "vram_gb": instance.get("memoryInGb", 0),
                "price_per_hour": instance.get("securePrice", 0.0),
                "availability_status": "available"
            })
        return normalized
