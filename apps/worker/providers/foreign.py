from typing import Any, Dict, List
from apps.worker.providers.common.base import BaseProviderCrawler

class XesktopCrawler(BaseProviderCrawler):
    @property
    def provider_slug(self) -> str:
        return "xesktop"

    async def fetch_raw_data(self) -> Any:
        # Mocking data based on user screenshot for xesktop.com
        return {
            "servers": [
                {"gpu": "2x RTX PRO 6000 Blackwell", "vram": "192GB", "price": 3.98},
                {"gpu": "RTX PRO 6000 Blackwell", "vram": "96GB", "price": 1.99},
                {"gpu": "Tesla V100", "vram": "16GB", "price": 5.49},
                {"gpu": "GTX 1080Ti", "vram": "11GB", "price": 3.99}
            ]
        }

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        return raw_data.get("servers", [])

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for instance in parsed_data:
            gpu_name = instance.get("gpu", "Unknown")
            # Parse VRAM number
            vram_str = instance.get("vram", "0GB").replace("GB", "")
            vram = int(vram_str) if vram_str.isdigit() else 0

            normalized.append({
                "provider": self.provider_slug,
                "gpu_model": gpu_name,
                "vram_gb": vram,
                "price_per_hour": instance.get("price", 0.0),
                "availability_status": "available",
                "provider_link": "https://xesktop.com/price/",
                "sys_ram_gb": 128,  # Mocked
                "tdp_w": 250        # Mocked
            })
        return normalized
