import os
import json
import glob
from typing import List, Dict, Any
from apps.api.core.config import settings

class SystemCodeService:
    @staticmethod
    async def get_codes_by_group(group_id: str) -> List[str]:
        if not settings.USE_REAL_DB:
            # DB 미사용 시 기본 메타데이터 반환 (Fallback)
            if group_id == "GPU_PROVIDER":
                return ["vast-ai", "runpod", "aws", "vessl", "gpuaas", "cloudv", "runyourai", "gabia", "ktcloud", "xesktop"]
            return []
            
        from sqlalchemy.ext.asyncio import AsyncSession
        from apps.api.core.database import AsyncSessionLocal
        from apps.api.models.system_code import SystemCode
        from sqlalchemy import select
        
        async with SessionLocal() as db:
            result = await db.execute(
                select(SystemCode.SYS_CD_ID)
                .where(SystemCode.SYS_GROUP_ID == group_id)
            )
            return list(result.scalars().all())


class DataService:
    """
    Data Access Layer that abstracts where data comes from.
    """
    @staticmethod
    async def get_latest_prices(hardware_type: str = "gpu") -> List[Dict[str, Any]]:
        if settings.USE_REAL_DB:
            from sqlalchemy.ext.asyncio import AsyncSession
            from apps.api.core.database import AsyncSessionLocal
            from apps.services.gpu.models_history import GpuPriceHistory
            from sqlalchemy import select, desc
            
            all_records = []
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(GpuPriceHistory)
                    .where(GpuPriceHistory.hw_typ == hardware_type)
                    .order_by(desc(GpuPriceHistory.ts))
                    .limit(500)
                )
                rows = result.scalars().all()
                for r in rows:
                    all_records.append({
                        "provider": r.prv_id,
                        "gpu_model": r.gpu_mdl,
                        "cpu_model": r.cpu_mdl,
                        "vram_gb": r.vram_gb,
                        "cores": r.core_cnt,
                        "price_per_hour": r.prc_ph,
                        "availability_status": r.avl_st,
                        "provider_link": r.prv_url,
                        "sys_ram_gb": r.sys_ram,
                        "tdp_w": r.tdp_w,
                    })
            return all_records
            
        # Serverless Mode: Read from JSON
        data_dir = settings.LOCAL_STORAGE_DIR
        if not os.path.exists(data_dir):
            return []

        all_records = []
        providers = await SystemCodeService.get_codes_by_group("GPU_PROVIDER")
        
        import re

        for provider in providers:
            files = glob.glob(os.path.join(data_dir, f"{provider}_*.json"))
            if not files:
                continue
                
            def _extract_ts(fpath):
                m = re.search(r'(\d{8}_\d{6})', os.path.basename(fpath))
                return m.group(1) if m else "00000000_000000"

            latest_file = max(files, key=_extract_ts)
            try:
                with open(latest_file, "r", encoding="utf-8") as f:
                    records = json.load(f)
                    for r in records:
                        if "provider" not in r:
                            r["provider"] = provider
                    all_records.extend(records)
            except Exception as e:
                print(f"Error reading {latest_file}: {e}")
                
        return all_records

    @staticmethod
    async def get_all_historical_prices(hardware_type: str = "gpu") -> List[Dict[str, Any]]:
        """
        Reads ALL JSON files from data directory to build complete historical time-series.
        Extracts collection timestamp from file names (e.g. provider_20260722_193345.json).
        """
        import re
        from datetime import datetime, timezone

        if settings.USE_REAL_DB:
            return await DataService.get_latest_prices(hardware_type)

        data_dir = settings.LOCAL_STORAGE_DIR
        if not os.path.exists(data_dir):
            return []

        all_records = []
        providers = await SystemCodeService.get_codes_by_group("GPU_PROVIDER")

        for provider in providers:
            files = glob.glob(os.path.join(data_dir, f"{provider}_*.json"))
            for file_path in files:
                filename = os.path.basename(file_path)
                match = re.search(r'(\d{8}_\d{6})', filename)
                file_dt = None
                if match:
                    try:
                        file_dt = datetime.strptime(match.group(1), "%Y%m%d_%H%M%S").replace(tzinfo=timezone.utc)
                    except Exception:
                        pass
                if not file_dt:
                    mtime = os.path.getmtime(file_path)
                    file_dt = datetime.fromtimestamp(mtime, tz=timezone.utc)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        records = json.load(f)
                        for r in records:
                            rec_copy = dict(r)
                            if "provider" not in rec_copy:
                                rec_copy["provider"] = provider
                            rec_copy["timestamp"] = file_dt
                            all_records.append(rec_copy)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

        return all_records

    @staticmethod
    def _parse_vram(gpu_name: str) -> int:
        import re
        match = re.search(r'(\d+)GB', gpu_name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 0

    @staticmethod
    def _normalize_gpu_name(name: str) -> str:
        name = name.upper()
        name = name.replace("NVIDIA ", "").replace("GEFORCE ", "").replace("TESLA ", "")
        name = name.replace("-PCIE", "").replace("-SXM4", "").replace("-SXM2", "").replace(" PCIE", "")
        import re
        name = re.sub(r'-\d+GB', '', name)
        name = re.sub(r' \d+GB', '', name)
        return name.strip()

    @staticmethod
    async def get_gpus_for_ui() -> List[Dict[str, Any]]:
        """Aggregates raw records into a nice structure for the UI dashboard."""
        from apps.api.core.traffic_service import traffic_service
        records = await DataService.get_latest_prices()
        traffic_data = traffic_service.get_all_traffic()
        
        gpu_map = {}
        for r in records:
            raw_name = r.get("gpu_model") or r.get("gpu_name") or "Unknown GPU"
            gpu_name = DataService._normalize_gpu_name(raw_name)
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
                    "popularity_score": traffic_data.get(gpu_name, 0),
                    "offers": []
                }
            
            avail = r.get("availability_status")
            is_avail = avail if isinstance(avail, bool) else (str(avail).lower() == "available")
            
            provider_name = r.get("provider", "Unknown")
            price = float(r.get("price_per_hour", 0.0))
            if price <= 0:
                continue
            
            existing_offer = next((o for o in gpu_map[gpu_name]["offers"] if o["provider"] == provider_name), None)
            
            if existing_offer:
                if price < existing_offer["price_per_hour"]:
                    existing_offer["price_per_hour"] = price
                    existing_offer["region"] = r.get("region", "global")
                    existing_offer["provider_link"] = r.get("provider_link")
            else:
                gpu_map[gpu_name]["offers"].append({
                    "provider": provider_name,
                    "price_per_hour": price,
                    "is_available": is_avail,
                    "region": r.get("region", "global"),
                    "provider_link": r.get("provider_link"),
                    "sys_ram_gb": r.get("sys_ram_gb"),
                    "tdp_w": r.get("tdp_w"),
                })
            
        return list(gpu_map.values())
        
    @staticmethod
    async def get_cpus_for_ui() -> List[Dict[str, Any]]:
        """Aggregates raw records into a nice structure for the CPU UI dashboard."""
        records = await DataService.get_latest_prices(hardware_type="cpu")
        
        cpu_map = {}
        for r in records:
            cpu_name = r.get("cpu_model") or "Unknown CPU"
            cores = r.get("cores", 0)
                
            if cpu_name not in cpu_map:
                cpu_map[cpu_name] = {
                    "id": cpu_name,
                    "name": cpu_name,
                    "vram_gb": r.get("sys_ram_gb") or 0, # reusing vram_gb field in UI for RAM for now
                    "popularity_score": 0,
                    "offers": []
                }
            
            avail = r.get("availability_status")
            is_avail = avail if isinstance(avail, bool) else (str(avail).lower() == "available")
            
            provider_name = r.get("provider", "Unknown")
            price = float(r.get("price_per_hour", 0.0))
            
            existing_offer = next((o for o in cpu_map[cpu_name]["offers"] if o["provider"] == provider_name), None)
            
            if existing_offer:
                if price < existing_offer["price_per_hour"]:
                    existing_offer["price_per_hour"] = price
                    existing_offer["region"] = r.get("region", "global")
                    existing_offer["provider_link"] = r.get("provider_link")
            else:
                cpu_map[cpu_name]["offers"].append({
                    "provider": provider_name,
                    "price_per_hour": price,
                    "is_available": is_avail,
                    "region": r.get("region", "global"),
                    "provider_link": r.get("provider_link"),
                    "sys_ram_gb": r.get("sys_ram_gb"),
                    "tdp_w": r.get("tdp_w"),
                })
            
        return list(cpu_map.values())

data_service = DataService()
