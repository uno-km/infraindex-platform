from typing import List, Dict, Any

class RunpodParser:
    @staticmethod
    def parse(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for gpu in raw_data:
            gpu_id = gpu.get("id")
            display_name = gpu.get("displayName")
            secure_price = gpu.get("securePrice")
            community_price = gpu.get("communityPrice")
            memory = gpu.get("memoryInGb")
            
            if not gpu_id or secure_price is None:
                continue
                
            # Add Secure Cloud pricing
            normalized.append({
                "provider": "runpod",
                "machine_type": display_name,
                "gpu_name": gpu_id,
                "gpu_count": 1,
                "hourly_price": float(secure_price),
                "plan_type": "secure_cloud",
                "raw_offer_id": f"{gpu_id}_secure"
            })
            
            # Add Community Cloud pricing if available
            if community_price is not None:
                normalized.append({
                    "provider": "runpod",
                    "machine_type": display_name,
                    "gpu_name": gpu_id,
                    "gpu_count": 1,
                    "hourly_price": float(community_price),
                    "plan_type": "community_cloud",
                    "raw_offer_id": f"{gpu_id}_community"
                })
                
        return normalized
