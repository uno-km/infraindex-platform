from fastapi import APIRouter, Request
from typing import List

from apps.api.core.data_service import data_service

router = APIRouter()

@router.get("/")
async def get_resources(request: Request):
    """Return resources. Handled CPU if prefix is /cpu."""
    path = request.url.path
    
    if "/cpu" in path:
        return [
            {
                "id": "c6g.2xlarge",
                "name": "AWS EC2 c6g.2xlarge (Graviton2)",
                "vram_gb": 16,
                "offers": [{"provider": "aws", "price_per_hour": 0.272, "is_available": True, "region": "Seoul", "provider_link": "https://aws.amazon.com/ec2"}]
            },
            {
                "id": "n2-standard-4",
                "name": "GCP n2-standard-4 (Intel Xeon)",
                "vram_gb": 16,
                "offers": [{"provider": "gcp", "price_per_hour": 0.194, "is_available": True, "region": "Seoul", "provider_link": "https://cloud.google.com/compute"}]
            },
            {
                "id": "F4s_v2",
                "name": "Azure F4s v2 (Intel Xeon)",
                "vram_gb": 8,
                "offers": [{"provider": "azure", "price_per_hour": 0.169, "is_available": True, "region": "Korea Central"}]
            },
            {
                "id": "g3.c4.m16",
                "name": "NCloud Standard g3 (Intel Xeon)",
                "vram_gb": 16,
                "offers": [{"provider": "ncloud", "price_per_hour": 0.150, "is_available": True, "region": "KR", "provider_link": "https://www.ncloud.com"}]
            }
        ]
    elif "/storage" in path:
        return [
            {
                "id": "gp3",
                "name": "AWS EBS gp3 (Block Storage)",
                "vram_gb": 1000,
                "offers": [{"provider": "aws", "price_per_hour": 0.118, "is_available": True, "region": "Seoul", "provider_link": "https://aws.amazon.com/ebs"}]
            },
            {
                "id": "pd-ssd",
                "name": "GCP Persistent Disk SSD",
                "vram_gb": 1000,
                "offers": [{"provider": "gcp", "price_per_hour": 0.204, "is_available": True, "region": "Seoul"}]
            },
            {
                "id": "premium-ssd",
                "name": "Azure Premium SSD",
                "vram_gb": 1024,
                "offers": [{"provider": "azure", "price_per_hour": 0.170, "is_available": True, "region": "Korea Central"}]
            },
            {
                "id": "b2-storage",
                "name": "Backblaze B2 (Object Storage)",
                "vram_gb": 1000,
                "offers": [{"provider": "backblaze", "price_per_hour": 0.005, "is_available": True, "region": "Global"}]
            }
        ]
    elif "/baremetal" in path:
        return [
            {
                "id": "i3.metal",
                "name": "AWS EC2 i3.metal (72 Cores)",
                "vram_gb": 512,
                "offers": [{"provider": "aws", "price_per_hour": 6.176, "is_available": True, "region": "Seoul"}]
            },
            {
                "id": "c2-metal-88",
                "name": "GCP c2-metal-88 (88 Cores)",
                "vram_gb": 352,
                "offers": [{"provider": "gcp", "price_per_hour": 4.900, "is_available": True, "region": "Seoul"}]
            },
            {
                "id": "bm-high-cpu",
                "name": "KT Cloud Baremetal (40 Cores)",
                "vram_gb": 192,
                "offers": [{"provider": "ktcloud", "price_per_hour": 2.500, "is_available": True, "region": "KR"}]
            }
        ]
    
    return []
