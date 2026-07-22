from typing import Any, Dict, List
from apps.worker.providers.common.base import BaseProviderCrawler

class AWSCrawler(BaseProviderCrawler):
    @property
    def provider_slug(self) -> str:
        return "aws"

    async def fetch_raw_data(self) -> Any:
        # AWS Pricing API is usually fetched via Boto3 or public JSON index
        # Scaffold for Phase 15
        return {"products": [{"sku": "P4d.24xlarge", "attributes": {"memory": "1152 GiB", "gpu": "A100"}}]}

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        return raw_data.get("products", [])

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for instance in parsed_data:
            normalized.append({
                "provider": self.provider_slug,
                "gpu_model": instance.get("attributes", {}).get("gpu"),
                "vram_gb": 320, # Simplified
                "price_per_hour": 32.77,
                "availability_status": "available",
                "provider_link": "https://aws.amazon.com/ec2/instance-types/p4/"
            })
        return normalized
