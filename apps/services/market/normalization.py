import re
from typing import Dict, Any

def normalize_product_name(raw_title: str) -> Dict[str, Any]:
    """
    원본 상품명을 입력받아 표준화된 상품 정보로 변환합니다.
    """
    title = raw_title.upper()
    
    # 1. GPU 정규화
    if "4090" in title:
        return {
            "manufacturer": "NVIDIA",
            "model_name": "RTX 4090",
            "product_line": "GeForce",
            "category": "GPU",
            "generation": "Ada Lovelace",
            "vram_gb": 24,
            "memory_type": "GDDR6X"
        }
    elif "H100" in title:
        return {
            "manufacturer": "NVIDIA",
            "model_name": "H100",
            "product_line": "Hopper",
            "category": "Server GPU",
            "generation": "Hopper",
            "vram_gb": 80,
            "memory_type": "HBM3"
        }
    elif "H200" in title:
        return {
            "manufacturer": "NVIDIA",
            "model_name": "H200",
            "product_line": "Hopper",
            "category": "Server GPU",
            "generation": "Hopper",
            "vram_gb": 141,
            "memory_type": "HBM3e"
        }
    elif "A100" in title:
        # Check VRAM
        vram = 80 if "80GB" in title else 40
        return {
            "manufacturer": "NVIDIA",
            "model_name": f"A100 {vram}GB",
            "product_line": "Ampere",
            "category": "Server GPU",
            "generation": "Ampere",
            "vram_gb": vram,
            "memory_type": "HBM2e"
        }
        
    # 2. CPU 정규화 (예시)
    elif "7950X" in title:
        return {
            "manufacturer": "AMD",
            "model_name": "Ryzen 9 7950X",
            "product_line": "Ryzen",
            "category": "CPU",
            "generation": "Zen 4",
            "vram_gb": None,
            "memory_type": None
        }
        
    # 기본값
    return {
        "manufacturer": "Unknown",
        "model_name": raw_title[:100],
        "product_line": None,
        "category": "Unknown",
        "generation": None,
        "vram_gb": None,
        "memory_type": None
    }
