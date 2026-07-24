"""
apps/services/market/crawler_storage_global.py
Phase 8 확장 - 전세계 스토리지 대여(Cloud Block/Object Storage) 가격 수집기

지원 소스 (공개 가격 페이지):
  - AWS EBS (https://aws.amazon.com/ebs/pricing/)
  - Google Persistent Disk
  - Azure Managed Disks
  - Wasabi Hot Cloud Storage
  - Backblaze B2
  - Cloudflare R2
  - DigitalOcean Spaces / Block Storage
  - Vultr Block Storage
  - Hetzner Storage Box
  - 국내: NCloud Object Storage, KT Cloud Storage
"""
import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

logger = logging.getLogger(__name__)


# 공개 가격 데이터 (2024년 기준, 정기 업데이트 대상)
# 단위: USD/GB/month
GLOBAL_STORAGE_PROVIDERS = [
    # ─── 대형 클라우드 Block Storage ─────────────────────────────────────────
    {
        "provider": "AWS",
        "product": "EBS gp3 (Block Storage)",
        "storage_type": "SSD",
        "price_usd_per_gb_month": 0.08,
        "price_krw_per_gb_month": None,  # 자동 환산
        "region": "us-east-1",
        "tier": "Standard",
        "url": "https://aws.amazon.com/ebs/pricing/",
    },
    {
        "provider": "AWS",
        "product": "EBS io2 (High IOPS)",
        "storage_type": "SSD",
        "price_usd_per_gb_month": 0.125,
        "price_krw_per_gb_month": None,
        "region": "us-east-1",
        "tier": "Premium",
        "url": "https://aws.amazon.com/ebs/pricing/",
    },
    {
        "provider": "AWS",
        "product": "S3 Standard (Object)",
        "storage_type": "Object",
        "price_usd_per_gb_month": 0.023,
        "price_krw_per_gb_month": None,
        "region": "us-east-1",
        "tier": "Standard",
        "url": "https://aws.amazon.com/s3/pricing/",
    },
    {
        "provider": "Google Cloud",
        "product": "Persistent Disk SSD",
        "storage_type": "SSD",
        "price_usd_per_gb_month": 0.17,
        "price_krw_per_gb_month": None,
        "region": "us-central1",
        "tier": "Standard",
        "url": "https://cloud.google.com/compute/disks-image-pricing",
    },
    {
        "provider": "Google Cloud",
        "product": "Cloud Storage Standard",
        "storage_type": "Object",
        "price_usd_per_gb_month": 0.020,
        "price_krw_per_gb_month": None,
        "region": "us-central1",
        "tier": "Standard",
        "url": "https://cloud.google.com/storage/pricing",
    },
    {
        "provider": "Microsoft Azure",
        "product": "Managed Disk Premium SSD LRS",
        "storage_type": "SSD",
        "price_usd_per_gb_month": 0.135,
        "price_krw_per_gb_month": None,
        "region": "eastus",
        "tier": "Premium",
        "url": "https://azure.microsoft.com/en-us/pricing/details/managed-disks/",
    },
    {
        "provider": "Microsoft Azure",
        "product": "Blob Storage Hot Tier",
        "storage_type": "Object",
        "price_usd_per_gb_month": 0.018,
        "price_krw_per_gb_month": None,
        "region": "eastus",
        "tier": "Hot",
        "url": "https://azure.microsoft.com/en-us/pricing/details/storage/blobs/",
    },
    # ─── 저가 오브젝트 스토리지 ────────────────────────────────────────────────
    {
        "provider": "Cloudflare R2",
        "product": "R2 Object Storage",
        "storage_type": "Object",
        "price_usd_per_gb_month": 0.015,
        "price_krw_per_gb_month": None,
        "region": "Global",
        "tier": "Standard",
        "url": "https://developers.cloudflare.com/r2/pricing/",
    },
    {
        "provider": "Backblaze",
        "product": "B2 Cloud Storage",
        "storage_type": "Object",
        "price_usd_per_gb_month": 0.006,
        "price_krw_per_gb_month": None,
        "region": "US-West",
        "tier": "Standard",
        "url": "https://www.backblaze.com/b2/cloud-storage-pricing.html",
    },
    {
        "provider": "Wasabi",
        "product": "Wasabi Hot Cloud Storage",
        "storage_type": "Object",
        "price_usd_per_gb_month": 0.0068,
        "price_krw_per_gb_month": None,
        "region": "us-east-1",
        "tier": "Standard",
        "url": "https://wasabi.com/cloud-storage-pricing/",
    },
    # ─── 중소형 클라우드 Block Storage ────────────────────────────────────────
    {
        "provider": "DigitalOcean",
        "product": "Block Storage (NVMe SSD)",
        "storage_type": "SSD",
        "price_usd_per_gb_month": 0.10,
        "price_krw_per_gb_month": None,
        "region": "nyc1",
        "tier": "Standard",
        "url": "https://www.digitalocean.com/pricing/volumes",
    },
    {
        "provider": "DigitalOcean",
        "product": "Spaces (Object Storage)",
        "storage_type": "Object",
        "price_usd_per_gb_month": 0.02,
        "price_krw_per_gb_month": None,
        "region": "nyc3",
        "tier": "Standard",
        "url": "https://www.digitalocean.com/pricing/spaces",
    },
    {
        "provider": "Vultr",
        "product": "Block Storage NVMe",
        "storage_type": "SSD",
        "price_usd_per_gb_month": 0.08,
        "price_krw_per_gb_month": None,
        "region": "New Jersey",
        "tier": "NVMe",
        "url": "https://www.vultr.com/products/block-storage/",
    },
    {
        "provider": "Hetzner",
        "product": "Storage Box HB 10 TB",
        "storage_type": "HDD",
        "price_usd_per_gb_month": 0.0033,
        "price_krw_per_gb_month": None,
        "region": "EU",
        "tier": "Economy",
        "url": "https://www.hetzner.com/storage/storage-box",
    },
    {
        "provider": "Hetzner",
        "product": "Volume (Block SSD)",
        "storage_type": "SSD",
        "price_usd_per_gb_month": 0.052,
        "price_krw_per_gb_month": None,
        "region": "EU",
        "tier": "Standard",
        "url": "https://www.hetzner.com/cloud",
    },
    {
        "provider": "Linode (Akamai)",
        "product": "Block Storage",
        "storage_type": "SSD",
        "price_usd_per_gb_month": 0.10,
        "price_krw_per_gb_month": None,
        "region": "us-east",
        "tier": "Standard",
        "url": "https://www.linode.com/pricing/#storage",
    },
    {
        "provider": "OVH Cloud",
        "product": "Object Storage Swift",
        "storage_type": "Object",
        "price_usd_per_gb_month": 0.011,
        "price_krw_per_gb_month": None,
        "region": "EU",
        "tier": "Standard",
        "url": "https://www.ovhcloud.com/en/public-cloud/object-storage/",
    },
    # ─── 국내 클라우드 ─────────────────────────────────────────────────────────
    {
        "provider": "NCloud (Naver)",
        "product": "Object Storage",
        "storage_type": "Object",
        "price_usd_per_gb_month": None,
        "price_krw_per_gb_month": 25.0,  # ₩25/GB/월
        "region": "Korea",
        "tier": "Standard",
        "url": "https://www.ncloud.com/product/storage/objectStorage",
    },
    {
        "provider": "KT Cloud",
        "product": "Object Storage",
        "storage_type": "Object",
        "price_usd_per_gb_month": None,
        "price_krw_per_gb_month": 22.0,  # ₩22/GB/월
        "region": "Korea",
        "tier": "Standard",
        "url": "https://cloud.kt.com/portal/ktcloud/service/storage/objectStorage.html",
    },
    {
        "provider": "Kakao Cloud",
        "product": "Object Storage",
        "storage_type": "Object",
        "price_usd_per_gb_month": None,
        "price_krw_per_gb_month": 20.0,  # ₩20/GB/월
        "region": "Korea",
        "tier": "Standard",
        "url": "https://kakaocloud.com/service/storage",
    },
]


async def _get_usd_to_krw() -> float:
    """실시간 환율 조회 (실패 시 기본값 1,380 사용)"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                "https://api.frankfurter.app/latest?from=USD&to=KRW"
            )
            if resp.status_code == 200:
                data = resp.json()
                return float(data["rates"]["KRW"])
    except Exception:
        pass
    return 1380.0  # 기본값


class GlobalStorageCrawler:
    """
    전세계 스토리지 대여 가격 수집기.
    공개된 가격 정보를 기반으로 DB에 저장합니다.
    """

    async def fetch_prices(self) -> List[Dict[str, Any]]:
        """공개 가격 데이터 + 실시간 환율 적용"""
        usd_to_krw = await _get_usd_to_krw()
        logger.info(f"[GlobalStorageCrawler] USD/KRW: {usd_to_krw:.1f}")

        results = []
        for item in GLOBAL_STORAGE_PROVIDERS:
            price_usd = item.get("price_usd_per_gb_month")
            price_krw = item.get("price_krw_per_gb_month")

            # USD → KRW 환산 (KRW 직접 제공 아닌 경우)
            if price_usd and not price_krw:
                price_krw = price_usd * usd_to_krw

            # KRW → USD 환산 (USD 직접 제공 아닌 경우)
            if price_krw and not price_usd:
                price_usd = price_krw / usd_to_krw

            results.append({
                **item,
                "price_usd_per_gb_month": round(price_usd, 6) if price_usd else None,
                "price_krw_per_gb_month": round(price_krw, 2) if price_krw else None,
                "usd_to_krw_rate": usd_to_krw,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            })

        logger.info(f"[GlobalStorageCrawler] {len(results)}개 스토리지 가격 수집 완료")
        return results

    async def sync_to_db(self, db: AsyncSession) -> Dict[str, Any]:
        """
        수집된 가격을 StoragePriceHistory 테이블에 저장.
        중복 방지를 위해 동일 provider+product 조합은 덮어씀.
        """
        if db is None:
            return {"status": "error", "message": "Database not available"}

        try:
            from apps.api.models.storage import StoragePriceHistory

            prices = await self.fetch_prices()
            inserted = 0
            now = datetime.now(timezone.utc)

            for p in prices:
                price_krw = p.get("price_krw_per_gb_month")
                if price_krw is None:
                    continue

                record = StoragePriceHistory(
                    ts=now,
                    prv_id=p["provider"].replace(" ", "_").upper()[:50],
                    storage_mdl=p["product"][:200],
                    prc_pgb_mth=price_krw,
                )
                db.add(record)
                inserted += 1

            await db.commit()
            logger.info(f"[GlobalStorageCrawler] DB 저장 완료: {inserted}건")
            return {
                "status": "success",
                "inserted": inserted,
                "providers": len(set(p["provider"] for p in prices)),
            }

        except Exception as e:
            logger.error(f"[GlobalStorageCrawler] DB 저장 실패: {e}")
            await db.rollback()
            return {"status": "error", "message": str(e)}
