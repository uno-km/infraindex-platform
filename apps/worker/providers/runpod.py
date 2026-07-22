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
        from apps.worker.core.hardware_specs import enrich_hardware_specs
        normalized = []
        for instance in parsed_data:
            gpu_name = instance.get("id", "Unknown")
            specs = enrich_hardware_specs(gpu_name)
            
            normalized.append({
                "gpu_model": gpu_name,
                "vram_gb": instance.get("memoryInGb", 0),
                "price_per_hour": instance.get("securePrice", 0.0),
                "availability_status": "available",
                "provider_link": "https://www.runpod.io/console/gpu-cloud",
                "sys_ram_gb": specs["sys_ram_gb"],
                "tdp_w": specs["tdp_w"]
            })
        return normalized
