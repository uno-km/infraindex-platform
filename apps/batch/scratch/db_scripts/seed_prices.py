import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from shared.db.session import AsyncSessionLocal
from shared.models.provider import Provider
from shared.models.hardware import GpuModel, GpuVariant
from shared.models.offering import InstanceOffering, OfferingGpuConfiguration, PricingPlan
from shared.models.observation import PriceObservation

async def seed_prices():
    async with AsyncSessionLocal() as session:
        try:
            # Fetch base entities
            vast_ai = (await session.execute(select(Provider).where(Provider.slug == "vast-ai"))).scalar_one()
            runpod = (await session.execute(select(Provider).where(Provider.slug == "runpod"))).scalar_one()
            
            h100_variant = (await session.execute(select(GpuVariant).where(GpuVariant.name == "H100 SXM 80GB"))).scalar_one()
            
            # Create Offering 1 (Vast.ai 8x H100)
            offering1 = InstanceOffering(
                provider_id=vast_ai.id,
                machine_type_name="8x H100 SXM (Vast)",
                includes_cpu=True,
                includes_ram=True,
                includes_local_storage=True
            )
            session.add(offering1)
            await session.flush()
            
            config1 = OfferingGpuConfiguration(offering_id=offering1.id, gpu_variant_id=h100_variant.id, count=8)
            plan1 = PricingPlan(offering_id=offering1.id, plan_type="on_demand")
            session.add_all([config1, plan1])
            await session.flush()
            
            obs1 = PriceObservation(
                pricing_plan_id=plan1.id,
                source_price=15.20,
                source_currency="USD",
                source_unit="hour",
                normalized_hourly_price=15.20,
                normalized_gpu_hour_price=1.90,
                normalized_vram_gb_hour_price=0.02375,
                normalized_monthly_price=11096.0,
                availability_status="available",
                collected_at=datetime.now(timezone.utc)
            )
            session.add(obs1)
            
            # Create Offering 2 (Runpod 8x H100)
            offering2 = InstanceOffering(
                provider_id=runpod.id,
                machine_type_name="8x H100 SXM (Runpod)",
                includes_cpu=True,
                includes_ram=True,
                includes_local_storage=True
            )
            session.add(offering2)
            await session.flush()
            
            config2 = OfferingGpuConfiguration(offering_id=offering2.id, gpu_variant_id=h100_variant.id, count=8)
            plan2 = PricingPlan(offering_id=offering2.id, plan_type="secure_cloud")
            session.add_all([config2, plan2])
            await session.flush()
            
            obs2 = PriceObservation(
                pricing_plan_id=plan2.id,
                source_price=22.40,
                source_currency="USD",
                source_unit="hour",
                normalized_hourly_price=22.40,
                normalized_gpu_hour_price=2.80,
                normalized_vram_gb_hour_price=0.035,
                normalized_monthly_price=16352.0,
                availability_status="available",
                collected_at=datetime.now(timezone.utc)
            )
            session.add(obs2)
            
            await session.commit()
            print("Successfully seeded mock prices!")
        except Exception as e:
            print(f"Error: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed_prices())
