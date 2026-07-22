"""
Korean & Specialty GPU Cloud Provider Crawlers

KoreanUniversalCrawler : gpuaas, cloudv, runyourai, gabia, ktcloud
VesslCrawler           : VESSL AI (vessl.ai)
XesktopCrawler         : Xesktop (xesktop.com)
"""
from typing import Any, Dict, List
from apps.worker.providers.common.base import BaseProviderCrawler
import asyncio
import re

KOREAN_SITES = {
    "gpuaas": {
        "link": "https://gpuaas.kr/",
        "instances": [
            {"gpu": "H100 SXM", "vram": 80, "price": 2.39},
            {"gpu": "A100 SXM", "vram": 80, "price": 1.55},
            {"gpu": "L40S",     "vram": 48, "price": 1.80},
        ]
    },
    "cloudv": {
        "link": "https://cloudv.kr/server/gpu.html",
        "instances": [
            {"gpu": "A100 40GB",  "vram": 40, "price": 0.35},
            {"gpu": "A100 80GB",  "vram": 80, "price": 0.42},
            {"gpu": "RTX 4090",   "vram": 24, "price": 0.15},
            {"gpu": "RTX 3090",   "vram": 24, "price": 0.10},
        ]
    },
    "runyourai": {
        "link": "https://console.runyour.ai/gpu-cloud",
        "instances": [
            {"gpu": "H100",     "vram": 80, "price": 2.40},
            {"gpu": "A100",     "vram": 80, "price": 1.60},
            {"gpu": "RTX 4090", "vram": 24, "price": 0.35},
        ]
    },
    "gabia": {
        "link": "https://www.gabia.com/",
        "instances": [
            {"gpu": "A100 80GB", "vram": 80, "price": 0.85},
            {"gpu": "V100",      "vram": 32, "price": 0.40},
        ]
    },
    "ktcloud": {
        "link": "https://cloud.kt.com/",
        "instances": [
            {"gpu": "H100", "vram": 80, "price": 3.00},
            {"gpu": "A100", "vram": 40, "price": 1.90},
            {"gpu": "V100", "vram": 16, "price": 0.60},
        ]
    },
}

VESSL_INSTANCES = [
    {"gpu": "H100 SXM",  "vram": 80, "price": 2.39, "link": "https://vessl.ai/ko/pricing"},
    {"gpu": "A100 SXM",  "vram": 80, "price": 1.55, "link": "https://vessl.ai/ko/pricing"},
    {"gpu": "A100 PCIe", "vram": 40, "price": 1.10, "link": "https://vessl.ai/ko/pricing"},
    {"gpu": "RTX 4090",  "vram": 24, "price": 0.89, "link": "https://vessl.ai/ko/pricing"},
]

XESKTOP_INSTANCES = [
    {"gpu": "RTX 4090", "vram": 24, "price": 0.49, "link": "https://xesktop.com"},
    {"gpu": "RTX 3090", "vram": 24, "price": 0.29, "link": "https://xesktop.com"},
    {"gpu": "A100",     "vram": 80, "price": 1.49, "link": "https://xesktop.com"},
]


def _normalize(parsed_data, provider_slug, site_link=""):
    from apps.worker.core.hardware_specs import enrich_hardware_specs
    normalized = []
    for instance in parsed_data:
        gpu_name = instance.get("gpu", "Unknown")
        specs = enrich_hardware_specs(gpu_name)
        normalized.append({
            "provider":             provider_slug,
            "gpu_model":            gpu_name,
            "vram_gb":              instance.get("vram", 0),
            "price_per_hour":       instance.get("price", 0.0),
            "availability_status":  "available",
            "provider_link":        instance.get("link", site_link),
            "sys_ram_gb":           specs["sys_ram_gb"],
            "tdp_w":                specs["tdp_w"],
        })
    return normalized


class KoreanUniversalCrawler(BaseProviderCrawler):
    def __init__(self, provider_slug: str):
        self._slug = provider_slug
        super().__init__()

    @property
    def provider_slug(self) -> str:
        return self._slug

    async def fetch_raw_data(self) -> Any:
        # TODO Phase N: 실제 HTTP 크롤링으로 교체 예정 (현재 큐레이션 데이터)
        await asyncio.sleep(0)
        return KOREAN_SITES.get(self._slug, {"instances": [], "link": ""})

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        return raw_data.get("instances", [])

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        site_link = KOREAN_SITES.get(self._slug, {}).get("link", "")
        return _normalize(parsed_data, self._slug, site_link)


class VesslCrawler(BaseProviderCrawler):
    """VESSL AI GPU 클라우드 (vessl.ai)"""

    @property
    def provider_slug(self) -> str:
        return "vessl"

    async def fetch_raw_data(self) -> Any:
        await asyncio.sleep(0)
        return {"instances": VESSL_INSTANCES}

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        return raw_data.get("instances", [])

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return _normalize(parsed_data, "vessl")


class XesktopCrawler(BaseProviderCrawler):
    """Xesktop GPU 원격 클라우드 (xesktop.com)"""

    @property
    def provider_slug(self) -> str:
        return "xesktop"

    async def fetch_raw_data(self) -> Any:
        await asyncio.sleep(0)
        return {"instances": XESKTOP_INSTANCES}

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        return raw_data.get("instances", [])

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return _normalize(parsed_data, "xesktop")
