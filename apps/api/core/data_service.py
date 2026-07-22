import os
import json
import glob
from typing import List, Dict, Any
from apps.api.core.config import settings

class DataService:
    """
    Data Access Layer that abstracts where data comes from.
    """
    @staticmethod
    async def get_latest_prices() -> List[Dict[str, Any]]:
        if settings.USE_REAL_DB:
            from sqlalchemy.ext.asyncio import AsyncSession
            from apps.api.core.database import SessionLocal
            from apps.api.models.history import PriceHistory
            from sqlalchemy import select, desc
            
            all_records = []
            async with SessionLocal() as db:
                # 간단히 최근 500개 레코드를 가져옵니다. 
                # (실제로는 provider, gpu별 최신값을 서브쿼리로 가져와야 함)
                result = await db.execute(
                    select(PriceHistory).order_by(desc(PriceHistory.timestamp)).limit(500)
                )
                rows = result.scalars().all()
                for r in rows:
                    all_records.append({
                        "provider": r.provider_id,
                        "gpu_model": r.gpu_model,
                        "vram_gb": r.vram_gb,
                        "price_per_hour": r.price_per_hour,
                        "availability_status": r.availability_status,
                        "provider_link": r.provider_link,
                        "sys_ram_gb": r.sys_ram_gb,
                        "tdp_w": r.tdp_w,
                    })
            return all_records
            
        # Serverless Mode: Read from JSON
        data_dir = settings.LOCAL_STORAGE_DIR
        if not os.path.exists(data_dir):
            return []

        all_records = []
        providers = ["vast-ai", "runpod", "aws", "vessl", "gpuaas", "cloudv", "runyourai", "gabia", "ktcloud"]
        
        for provider in providers:
            files = glob.glob(os.path.join(data_dir, f"{provider}_*.json"))
            if not files:
                continue
                
            latest_file = max(files, key=os.path.getctime)
            try:
                with open(latest_file, "r", encoding="utf-8") as f:
                    records = json.load(f)
                    # JSON에는 provider 필드가 없을 수 있으므로 주입
                    for r in records:
                        if "provider" not in r:
                            r["provider"] = provider
                    all_records.extend(records)
            except Exception as e:
                print(f"Error reading {latest_file}: {e}")
                
        return all_records

    @staticmethod
    def _parse_vram(gpu_name: str) -> int:
        import re
        match = re.search(r'(\d+)GB', gpu_name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 0

    @staticmethod
    async def get_gpus_for_ui() -> List[Dict[str, Any]]:
        """Aggregates raw records into a nice structure for the UI dashboard."""
        records = await DataService.get_latest_prices()
        
        gpu_map = {}
        for r in records:
            gpu_name = r.get("gpu_model") or r.get("gpu_name") or "Unknown GPU"
            vram = r.get("vram_gb")
            if vram:
                vram = round(float(vram))
            else:
                vram = DataService._parse_vram(gpu_name)
                
            if gpu_name not in gpu_map:
                gpu_map[gpu_name] = {
                    "id": gpu_name,
                    "name": gpu_name,
                    "vram_gb": vram,
                    "offers": []
                }
            
            avail = r.get("availability_status")
            is_avail = avail if isinstance(avail, bool) else (str(avail).lower() == "available")
            
            gpu_map[gpu_name]["offers"].append({
                "provider": r.get("provider", "Unknown"),
                "price_per_hour": float(r.get("price_per_hour", 0.0)),
                "is_available": is_avail,
                "region": r.get("region", "global"),
                "provider_link": r.get("provider_link"),
                "sys_ram_gb": r.get("sys_ram_gb"),
                "tdp_w": r.get("tdp_w"),
            })
            
        return list(gpu_map.values())

data_service = DataService()
