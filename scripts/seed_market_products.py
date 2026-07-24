"""
scripts/seed_market_products.py
소매 시세표용 RAM/SSD/Server GPU/GPU 초기 데이터 시딩 스크립트

사용법:
    python scripts/seed_market_products.py
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed")

# 시딩 데이터 정의
SEED_PRODUCTS = [
    # ────── GPU (소비자용) ──────────────────────────────────────────────────
    {"manufacturer": "NVIDIA", "model_name": "GeForce RTX 4090", "category": "GPU", "product_line": "GeForce RTX 40", "vram_gb": 24, "memory_type": "GDDR6X"},
    {"manufacturer": "NVIDIA", "model_name": "GeForce RTX 4080 SUPER", "category": "GPU", "product_line": "GeForce RTX 40", "vram_gb": 16, "memory_type": "GDDR6X"},
    {"manufacturer": "NVIDIA", "model_name": "GeForce RTX 4080", "category": "GPU", "product_line": "GeForce RTX 40", "vram_gb": 16, "memory_type": "GDDR6X"},
    {"manufacturer": "NVIDIA", "model_name": "GeForce RTX 4070 Ti SUPER", "category": "GPU", "product_line": "GeForce RTX 40", "vram_gb": 16, "memory_type": "GDDR6X"},
    {"manufacturer": "NVIDIA", "model_name": "GeForce RTX 4070 Ti", "category": "GPU", "product_line": "GeForce RTX 40", "vram_gb": 12, "memory_type": "GDDR6X"},
    {"manufacturer": "NVIDIA", "model_name": "GeForce RTX 4070 SUPER", "category": "GPU", "product_line": "GeForce RTX 40", "vram_gb": 12, "memory_type": "GDDR6X"},
    {"manufacturer": "NVIDIA", "model_name": "GeForce RTX 4070", "category": "GPU", "product_line": "GeForce RTX 40", "vram_gb": 12, "memory_type": "GDDR6X"},
    {"manufacturer": "NVIDIA", "model_name": "GeForce RTX 4060 Ti", "category": "GPU", "product_line": "GeForce RTX 40", "vram_gb": 16, "memory_type": "GDDR6"},
    {"manufacturer": "NVIDIA", "model_name": "GeForce RTX 4060", "category": "GPU", "product_line": "GeForce RTX 40", "vram_gb": 8, "memory_type": "GDDR6"},
    {"manufacturer": "NVIDIA", "model_name": "GeForce RTX 5090", "category": "GPU", "product_line": "GeForce RTX 50", "vram_gb": 32, "memory_type": "GDDR7"},
    {"manufacturer": "NVIDIA", "model_name": "GeForce RTX 5080", "category": "GPU", "product_line": "GeForce RTX 50", "vram_gb": 16, "memory_type": "GDDR7"},
    {"manufacturer": "AMD", "model_name": "Radeon RX 7900 XTX", "category": "GPU", "product_line": "Radeon RX 7000", "vram_gb": 24, "memory_type": "GDDR6"},
    {"manufacturer": "AMD", "model_name": "Radeon RX 7900 XT", "category": "GPU", "product_line": "Radeon RX 7000", "vram_gb": 20, "memory_type": "GDDR6"},
    {"manufacturer": "AMD", "model_name": "Radeon RX 7800 XT", "category": "GPU", "product_line": "Radeon RX 7000", "vram_gb": 16, "memory_type": "GDDR6"},
    {"manufacturer": "AMD", "model_name": "Radeon RX 9070 XT", "category": "GPU", "product_line": "Radeon RX 9000", "vram_gb": 16, "memory_type": "GDDR6"},

    # ────── Server GPU ──────────────────────────────────────────────────────
    {"manufacturer": "NVIDIA", "model_name": "H100 SXM5 80GB", "category": "SERVER_GPU", "product_line": "Hopper", "vram_gb": 80, "memory_type": "HBM3"},
    {"manufacturer": "NVIDIA", "model_name": "H100 PCIe 80GB", "category": "SERVER_GPU", "product_line": "Hopper", "vram_gb": 80, "memory_type": "HBM2e"},
    {"manufacturer": "NVIDIA", "model_name": "H200 SXM5 141GB", "category": "SERVER_GPU", "product_line": "Hopper", "vram_gb": 141, "memory_type": "HBM3e"},
    {"manufacturer": "NVIDIA", "model_name": "A100 SXM4 80GB", "category": "SERVER_GPU", "product_line": "Ampere", "vram_gb": 80, "memory_type": "HBM2e"},
    {"manufacturer": "NVIDIA", "model_name": "A100 PCIe 40GB", "category": "SERVER_GPU", "product_line": "Ampere", "vram_gb": 40, "memory_type": "HBM2"},
    {"manufacturer": "NVIDIA", "model_name": "L40S 48GB", "category": "SERVER_GPU", "product_line": "Ada Lovelace", "vram_gb": 48, "memory_type": "GDDR6"},
    {"manufacturer": "NVIDIA", "model_name": "RTX 6000 Ada 48GB", "category": "SERVER_GPU", "product_line": "Ada Lovelace", "vram_gb": 48, "memory_type": "GDDR6"},
    {"manufacturer": "AMD", "model_name": "Instinct MI300X 192GB", "category": "SERVER_GPU", "product_line": "CDNA3", "vram_gb": 192, "memory_type": "HBM3"},
    {"manufacturer": "AMD", "model_name": "Instinct MI250X 128GB", "category": "SERVER_GPU", "product_line": "CDNA2", "vram_gb": 128, "memory_type": "HBM2e"},

    # ────── RAM ──────────────────────────────────────────────────────────────
    {"manufacturer": "Samsung", "model_name": "DDR5-6400 32GB", "category": "RAM", "product_line": "DDR5", "vram_gb": 32, "memory_type": "DDR5"},
    {"manufacturer": "Samsung", "model_name": "DDR5-5600 16GB", "category": "RAM", "product_line": "DDR5", "vram_gb": 16, "memory_type": "DDR5"},
    {"manufacturer": "SK Hynix", "model_name": "DDR5-6400 32GB", "category": "RAM", "product_line": "DDR5", "vram_gb": 32, "memory_type": "DDR5"},
    {"manufacturer": "SK Hynix", "model_name": "DDR5-5600 16GB", "category": "RAM", "product_line": "DDR5", "vram_gb": 16, "memory_type": "DDR5"},
    {"manufacturer": "Micron", "model_name": "DDR5-6400 32GB", "category": "RAM", "product_line": "DDR5", "vram_gb": 32, "memory_type": "DDR5"},
    {"manufacturer": "G.Skill", "model_name": "Trident Z5 DDR5-7200 32GB", "category": "RAM", "product_line": "Trident Z5", "vram_gb": 32, "memory_type": "DDR5"},
    {"manufacturer": "G.Skill", "model_name": "Trident Z5 DDR5-6000 16GB", "category": "RAM", "product_line": "Trident Z5", "vram_gb": 16, "memory_type": "DDR5"},
    {"manufacturer": "Corsair", "model_name": "Vengeance DDR5-6000 32GB", "category": "RAM", "product_line": "Vengeance", "vram_gb": 32, "memory_type": "DDR5"},
    {"manufacturer": "Samsung", "model_name": "DDR4-3200 16GB", "category": "RAM", "product_line": "DDR4", "vram_gb": 16, "memory_type": "DDR4"},
    {"manufacturer": "SK Hynix", "model_name": "DDR4-3200 8GB", "category": "RAM", "product_line": "DDR4", "vram_gb": 8, "memory_type": "DDR4"},

    # ────── SSD ──────────────────────────────────────────────────────────────
    {"manufacturer": "Samsung", "model_name": "990 Pro 2TB NVMe", "category": "SSD", "product_line": "990 Pro", "vram_gb": 2000, "memory_type": "TLC"},
    {"manufacturer": "Samsung", "model_name": "990 Pro 1TB NVMe", "category": "SSD", "product_line": "990 Pro", "vram_gb": 1000, "memory_type": "TLC"},
    {"manufacturer": "Samsung", "model_name": "870 EVO 4TB SATA", "category": "SSD", "product_line": "870 EVO", "vram_gb": 4000, "memory_type": "MLC"},
    {"manufacturer": "SK Hynix", "model_name": "Platinum P41 2TB NVMe", "category": "SSD", "product_line": "Platinum P41", "vram_gb": 2000, "memory_type": "176L TLC"},
    {"manufacturer": "WD", "model_name": "Black SN850X 2TB NVMe", "category": "SSD", "product_line": "Black SN850X", "vram_gb": 2000, "memory_type": "TLC"},
    {"manufacturer": "WD", "model_name": "Black SN850X 1TB NVMe", "category": "SSD", "product_line": "Black SN850X", "vram_gb": 1000, "memory_type": "TLC"},
    {"manufacturer": "Seagate", "model_name": "FireCuda 530 4TB NVMe", "category": "SSD", "product_line": "FireCuda 530", "vram_gb": 4000, "memory_type": "TLC"},
    {"manufacturer": "Kingston", "model_name": "KC3000 2TB NVMe", "category": "SSD", "product_line": "KC3000", "vram_gb": 2000, "memory_type": "TLC"},
    {"manufacturer": "Micron", "model_name": "3400 2TB NVMe", "category": "SSD", "product_line": "3400", "vram_gb": 2000, "memory_type": "TLC"},
]


async def seed():
    from apps.api.core.database import AsyncSessionLocal
    from apps.api.models.market import MarketProduct
    from sqlalchemy.future import select

    async with AsyncSessionLocal() as db:
        # 기존 제품 목록 조회
        result = await db.execute(select(MarketProduct.model_name, MarketProduct.manufacturer))
        existing = {(r.manufacturer, r.model_name) for r in result.all()}
        logger.info(f"기존 제품 수: {len(existing)}")

        added = 0
        for item in SEED_PRODUCTS:
            key = (item["manufacturer"], item["model_name"])
            if key in existing:
                continue
            product = MarketProduct(
                manufacturer=item["manufacturer"],
                model_name=item["model_name"],
                category=item["category"],
                product_line=item.get("product_line", ""),
                vram_gb=item.get("vram_gb"),
                memory_type=item.get("memory_type", ""),
            )
            db.add(product)
            added += 1

        await db.commit()
        logger.info(f"시딩 완료: {added}개 신규 제품 추가 (총 {len(SEED_PRODUCTS)}개 정의)")


if __name__ == "__main__":
    asyncio.run(seed())
