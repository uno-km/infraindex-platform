"""
P2-001: AWS GPU 인스턴스 가격 크롤러 — 실제 구현

전략:
  1. AWS 공개 Pricing JSON 인덱스에서 EC2 GPU 인스턴스 목록 + 가격 수집
     (인증 불필요, 완전 공개 엔드포인트)
  2. GPU 인스턴스 계열 필터: p4, p3, g5, g4, trn 시리즈
  3. On-Demand 리눅스 가격만 추출
  4. HTTP 실패 시 공개 가격 표 기반 큐레이션 데이터로 폴백

AWS 공개 Pricing JSON URL:
  https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json
  (파일이 수 GB이므로, region-specific JSON 사용)
  https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/<region>/index.json
"""

import logging
import re
from typing import Any, Dict, List

import httpx
from apps.worker.providers.common.base import BaseProviderCrawler

logger = logging.getLogger(__name__)

# GPU 인스턴스 계열 — On-Demand 가격 수집 대상
GPU_INSTANCE_PREFIXES = ("p4d", "p4de", "p3", "p3dn", "g5", "g4dn", "g4ad", "trn1", "inf2")

# AWS Pricing JSON 엔드포인트 (리전별 파일 — 전체보다 훨씬 작음)
PRICING_REGION = "ap-northeast-2"  # Seoul — 기본 리전
PRICING_URL = (
    f"https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2"
    f"/current/{PRICING_REGION}/index.json"
)

# 폴백: 공개 가격 표 기반 큐레이션 (2025년 기준 ap-northeast-2 On-Demand)
FALLBACK_GPU_INSTANCES: List[Dict] = [
    {"instance": "p4d.24xlarge",  "gpu": "A100",      "gpu_count": 8,  "vram_gb": 320, "price_usd": 32.7726},
    {"instance": "p3.2xlarge",    "gpu": "V100",       "gpu_count": 1,  "vram_gb": 16,  "price_usd": 3.823},
    {"instance": "p3.8xlarge",    "gpu": "V100",       "gpu_count": 4,  "vram_gb": 64,  "price_usd": 15.292},
    {"instance": "p3.16xlarge",   "gpu": "V100",       "gpu_count": 8,  "vram_gb": 128, "price_usd": 30.584},
    {"instance": "p3dn.24xlarge", "gpu": "V100",       "gpu_count": 8,  "vram_gb": 256, "price_usd": 35.894},
    {"instance": "g5.xlarge",     "gpu": "A10G",       "gpu_count": 1,  "vram_gb": 24,  "price_usd": 1.323},
    {"instance": "g5.2xlarge",    "gpu": "A10G",       "gpu_count": 1,  "vram_gb": 24,  "price_usd": 1.515},
    {"instance": "g5.12xlarge",   "gpu": "A10G",       "gpu_count": 4,  "vram_gb": 96,  "price_usd": 8.228},
    {"instance": "g5.48xlarge",   "gpu": "A10G",       "gpu_count": 8,  "vram_gb": 192, "price_usd": 22.532},
    {"instance": "g4dn.xlarge",   "gpu": "T4",         "gpu_count": 1,  "vram_gb": 16,  "price_usd": 0.752},
    {"instance": "g4dn.12xlarge", "gpu": "T4",         "gpu_count": 4,  "vram_gb": 64,  "price_usd": 5.656},
    {"instance": "trn1.2xlarge",  "gpu": "Trainium",   "gpu_count": 1,  "vram_gb": 32,  "price_usd": 1.343},
    {"instance": "trn1.32xlarge", "gpu": "Trainium",   "gpu_count": 16, "vram_gb": 512, "price_usd": 21.500},
    {"instance": "inf2.xlarge",   "gpu": "Inferentia2","gpu_count": 1,  "vram_gb": 32,  "price_usd": 0.758},
    {"instance": "inf2.48xlarge", "gpu": "Inferentia2","gpu_count": 12, "vram_gb": 384, "price_usd": 13.617},
]


class AWSCrawler(BaseProviderCrawler):
    """
    AWS EC2 GPU 인스턴스 On-Demand 가격 크롤러.
    AWS 공개 Pricing JSON API 사용 → 실패 시 큐레이션 폴백.
    """

    @property
    def provider_slug(self) -> str:
        return "aws"

    async def fetch_raw_data(self) -> Any:
        """
        AWS Pricing JSON API에서 ap-northeast-2 EC2 가격 데이터 수집.
        파일이 크므로 타임아웃 60초 설정.
        """
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                logger.info(f"[aws] Fetching pricing JSON from {PRICING_URL}")
                resp = await client.get(PRICING_URL)
                resp.raise_for_status()
                logger.info(f"[aws] Pricing JSON received ({len(resp.content) // 1024} KB)")
                return resp.json()
        except Exception as e:
            logger.warning(f"[aws] Pricing API fetch failed: {e}. Using curated fallback.")
            return {"__fallback__": True}

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        # 폴백 모드
        if raw_data.get("__fallback__"):
            logger.info("[aws] Parsing curated fallback data.")
            return FALLBACK_GPU_INSTANCES

        products = raw_data.get("products", {})
        terms = raw_data.get("terms", {}).get("OnDemand", {})

        gpu_products = []
        for sku, product in products.items():
            attrs = product.get("attributes", {})
            instance_type = attrs.get("instanceType", "")

            # GPU 인스턴스 계열만 필터
            if not any(instance_type.startswith(p) for p in GPU_INSTANCE_PREFIXES):
                continue
            # 리눅스 On-Demand만
            if attrs.get("operatingSystem", "").lower() != "linux":
                continue
            if attrs.get("tenancy", "").lower() != "shared":
                continue
            if attrs.get("preInstalledSw", "").lower() != "na":
                continue

            # On-Demand 가격 추출
            sku_terms = terms.get(sku, {})
            price_usd = self._extract_on_demand_price(sku_terms)
            if price_usd is None or price_usd <= 0:
                continue

            gpu_info = attrs.get("gpu", "0")
            try:
                gpu_count = int(gpu_info)
            except ValueError:
                gpu_count = 1

            gpu_memory_raw = attrs.get("gpuMemory", "0 GiB")
            vram_gb = self._parse_gib(gpu_memory_raw)

            gpu_products.append({
                "instance":   instance_type,
                "gpu":        self._infer_gpu_name(instance_type, attrs),
                "gpu_count":  gpu_count,
                "vram_gb":    vram_gb,
                "price_usd":  price_usd,
            })

        logger.info(f"[aws] Parsed {len(gpu_products)} GPU On-Demand products from pricing JSON.")
        return gpu_products

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        from apps.worker.core.hardware_specs import enrich_hardware_specs
        normalized = []
        for item in parsed_data:
            gpu_count = item.get("gpu_count", 1)
            total_price = float(item.get("price_usd", 0.0))
            vram = float(item.get("vram_gb", 0.0))
            gpu_name = item.get("gpu", "Unknown")
            instance_type = item.get("instance", "")

            # GPU당 가격으로 환산
            price_per_gpu_per_hour = round(total_price / max(gpu_count, 1), 4)
            specs = enrich_hardware_specs(gpu_name)

            normalized.append({
                "gpu_model":           gpu_name,
                "vram_gb":             vram / max(gpu_count, 1),
                "price_per_hour":      price_per_gpu_per_hour,
                "availability_status": "available",
                "provider":            "aws",
                "provider_link":       f"https://aws.amazon.com/ec2/instance-types/{instance_type.split('.')[0]}/",
                "instance_type":       instance_type,
                "gpu_count":           gpu_count,
                "sys_ram_gb":          specs["sys_ram_gb"],
                "tdp_w":               specs["tdp_w"],
            })
        return normalized

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _extract_on_demand_price(sku_terms: Dict) -> float | None:
        """SKU On-Demand 조건에서 USD/hr 가격 추출."""
        for offer in sku_terms.values():
            for dim in offer.get("priceDimensions", {}).values():
                usd_str = dim.get("pricePerUnit", {}).get("USD", "0")
                try:
                    price = float(usd_str)
                    if price > 0:
                        return price
                except ValueError:
                    pass
        return None

    @staticmethod
    def _parse_gib(text: str) -> float:
        """'320 GiB' → 320.0"""
        match = re.search(r"([\d.]+)", text.replace(",", ""))
        return float(match.group(1)) if match else 0.0

    @staticmethod
    def _infer_gpu_name(instance_type: str, attrs: Dict) -> str:
        """인스턴스 타입과 attrs에서 GPU 이름 추론."""
        prefix = instance_type.split(".")[0].lower()
        gpu_map = {
            "p4d":  "A100",
            "p4de": "A100",
            "p3":   "V100",
            "p3dn": "V100",
            "g5":   "A10G",
            "g4dn": "T4",
            "g4ad": "Radeon Pro V520",
            "trn1": "Trainium",
            "inf2": "Inferentia2",
        }
        if prefix in gpu_map:
            return gpu_map[prefix]
        # attrs 직접 확인
        return attrs.get("gpu", attrs.get("processorFeatures", "Unknown GPU"))
