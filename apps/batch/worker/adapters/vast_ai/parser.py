from typing import List, Dict, Any

class VastAiParser:
    @staticmethod
    def parse(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for offer in raw_data:
            # Safely extract fields using Vast.ai's schema
            machine_id = offer.get("machine_id")
            gpu_name = offer.get("gpu_name")
            num_gpus = offer.get("num_gpus", 1)
            dph_base = offer.get("dph_base") # Price per hour
            
            if not machine_id or not gpu_name or dph_base is None:
                continue
                
            normalized.append({
                "provider": "vast-ai",
                "machine_type": f"{num_gpus}x {gpu_name}",
                "gpu_name": gpu_name,
                "gpu_count": num_gpus,
                "hourly_price": float(dph_base),
                "raw_offer_id": str(machine_id)
            })
            
        return normalized
