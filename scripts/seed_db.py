import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from apps.api.core.database import AsyncSessionLocal
from apps.api.models.provider import Provider
from apps.api.models.hardware import GpuManufacturer, GpuModel, GpuVariant

async def seed():
    async with AsyncSessionLocal() as session:
        # Check if already seeded
        try:
            # Seed Providers
            providers = [
                Provider(name="Vast.ai", slug="vast-ai"),
                Provider(name="Runpod", slug="runpod"),
                Provider(name="Lambda Labs", slug="lambda-labs"),
            ]
            session.add_all(providers)
            
            # Seed GPU Manufacturers
            nvidia = GpuManufacturer(name="NVIDIA")
            amd = GpuManufacturer(name="AMD")
            session.add_all([nvidia, amd])
            
            await session.commit()
            
            # Seed GPU Models
            h100 = GpuModel(name="H100", manufacturer_id=nvidia.id)
            a100 = GpuModel(name="A100", manufacturer_id=nvidia.id)
            rtx4090 = GpuModel(name="RTX 4090", manufacturer_id=nvidia.id)
            session.add_all([h100, a100, rtx4090])
            
            await session.commit()
            
            # Seed Variants
            session.add_all([
                GpuVariant(name="H100 SXM 80GB", model_id=h100.id, form_factor="SXM", vram_gb=80.0),
                GpuVariant(name="H100 PCIe 80GB", model_id=h100.id, form_factor="PCIe", vram_gb=80.0),
                GpuVariant(name="A100 SXM4 80GB", model_id=a100.id, form_factor="SXM", vram_gb=80.0),
                GpuVariant(name="A100 PCIe 80GB", model_id=a100.id, form_factor="PCIe", vram_gb=80.0),
                GpuVariant(name="RTX 4090 24GB", model_id=rtx4090.id, form_factor="PCIe", vram_gb=24.0),
            ])
            
            await session.commit()
            print("Successfully seeded database!")
        except Exception as e:
            print(f"Error seeding database (maybe already seeded?): {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed())
