from typing import Any, Dict, List
from apps.worker.providers.common.base import BaseProviderCrawler

class VastCrawler(BaseProviderCrawler):
    @property
    def provider_slug(self) -> str:
        return "vast-ai"

    async def fetch_raw_data(self) -> Any:
        # Utilizing StealthHttpClient
        client = await self.http.get_client()
        response = await client.get("https://console.vast.ai/api/v0/bundles/")
        return response.json() if response.status_code == 200 else {}

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        offers = raw_data.get("offers", [])
        return offers

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for instance in parsed_data:
            gpu_name = instance.get("gpu_name")
            if not gpu_name:
                continue
                
            normalized.append({
                "gpu_model": gpu_name,
                "vram_gb": instance.get("gpu_ram", 0) / 1024.0,
                "price_per_hour": instance.get("dph_total", 0.0),
                "availability_status": "available" if instance.get("rentable") else "unavailable"
            })
        return normalized
