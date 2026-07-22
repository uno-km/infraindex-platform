from typing import Any, Dict, List
from apps.worker.providers.common.base import BaseProviderCrawler
import asyncio

KOREAN_SITES = {
    "vessl": {
        "link": "https://vessl.ai/ko/pricing",
        "instances": [
            {"gpu": "H100 SXM", "vram": 80, "price": 2.39},
            {"gpu": "A100 SXM", "vram": 80, "price": 1.55},
            {"gpu": "A100 PCIe", "vram": 40, "price": 1.10},
        ]
    },
    "gpuaas": {
        "link": "https://gpuaas.kr/",
        "instances": [
            {"gpu": "H100 SXM", "vram": 80, "price": 2.39},
            {"gpu": "A100 SXM", "vram": 80, "price": 1.55},
            {"gpu": "L40S", "vram": 48, "price": 1.80},
        ]
    },
    "cloudv": {
        "link": "https://cloudv.kr/server/gpu.html",
        "instances": [
            {"gpu": "A100 40GB", "vram": 40, "price": 0.35},
            {"gpu": "A100 80GB", "vram": 80, "price": 0.42},
            {"gpu": "RTX 4090", "vram": 24, "price": 0.15},
            {"gpu": "RTX 3090", "vram": 24, "price": 0.10},
        ]
    },
    "runyourai": {
        "link": "https://console.runyour.ai/gpu-cloud",
        "instances": [
            {"gpu": "H100", "vram": 80, "price": 2.40},
            {"gpu": "A100", "vram": 80, "price": 1.60},
            {"gpu": "RTX 4090", "vram": 24, "price": 0.35},
        ]
    },
    "gabia": {
        "link": "https://www.gabia.com/",
        "instances": [
            {"gpu": "A100 80GB", "vram": 80, "price": 0.85},
            {"gpu": "V100", "vram": 32, "price": 0.40},
        ]
    },
    "ktcloud": {
        "link": "https://cloud.kt.com/",
        "instances": [
            {"gpu": "H100", "vram": 80, "price": 3.00},
            {"gpu": "A100", "vram": 40, "price": 1.90},
            {"gpu": "V100", "vram": 16, "price": 0.60},
        ]
    }
}

class KoreanUniversalCrawler(BaseProviderCrawler):
    def __init__(self, provider_slug: str):
        self._slug = provider_slug
        super().__init__()
        
    @property
    def provider_slug(self) -> str:
        return self._slug

    async def fetch_raw_data(self) -> Any:
        # Simulate network fetch for the site
        await asyncio.sleep(0.5)
        return KOREAN_SITES.get(self._slug, {"instances": []})

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        return raw_data.get("instances", [])

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        from apps.worker.core.hardware_specs import enrich_hardware_specs
        normalized = []
        site_info = KOREAN_SITES.get(self._slug, {})
        
        for instance in parsed_data:
            gpu_name = instance.get("gpu", "Unknown")
            specs = enrich_hardware_specs(gpu_name)
            
            normalized.append({
                "gpu_model": gpu_name,
                "vram_gb": instance.get("vram", 0),
                "price_per_hour": instance.get("price", 0.0),
                "availability_status": "available",
                "provider_link": site_info.get("link", "#"),
                "sys_ram_gb": specs["sys_ram_gb"],
                "tdp_w": specs["tdp_w"]
            })
        return normalized
