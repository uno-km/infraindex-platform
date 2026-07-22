import os
import json
import glob
from typing import List, Dict, Any
from apps.api.core.config import settings

class DataService:
    """
    Data Access Layer that abstracts where data comes from.
    If USE_REAL_DB is False, it reads from the latest JSON files in data/.
    """
    @staticmethod
    async def get_latest_prices() -> List[Dict[str, Any]]:
        if settings.USE_REAL_DB:
            # TODO: Implement Postgres reading logic
            return []
            
        # Serverless Mode: Read from JSON
        data_dir = settings.LOCAL_STORAGE_DIR
        if not os.path.exists(data_dir):
            return []

        all_records = []
        providers = ["vast-ai", "runpod", "aws"]
        
        for provider in providers:
            # Find the most recent file for the provider
            files = glob.glob(os.path.join(data_dir, f"{provider}_*.json"))
            if not files:
                continue
                
            latest_file = max(files, key=os.path.getctime)
            try:
                with open(latest_file, "r", encoding="utf-8") as f:
                    records = json.load(f)
                    all_records.extend(records)
            except Exception as e:
                print(f"Error reading {latest_file}: {e}")
                
        return all_records

    @staticmethod
    def _parse_vram(gpu_name: str) -> int:
        """Heuristic to extract VRAM from GPU name if possible."""
        # Simple extraction for UI purposes
        import re
        match = re.search(r'(\d+)GB', gpu_name, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 0

    @staticmethod
    async def get_gpus_for_ui() -> List[Dict[str, Any]]:
        """Aggregates raw records into a nice structure for the UI dashboard."""
        records = await DataService.get_latest_prices()
        
        # Group by GPU Name
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
            
            # Availability status could be boolean or string
            avail = r.get("availability_status")
            is_avail = avail if isinstance(avail, bool) else (str(avail).lower() == "available")
            
            gpu_map[gpu_name]["offers"].append({
                "provider": r.get("provider", "Unknown"),
                "price_per_hour": float(r.get("price_per_hour", 0.0)),
                "is_available": is_avail,
                "region": r.get("region", "global")
            })
            
        return list(gpu_map.values())

data_service = DataService()
