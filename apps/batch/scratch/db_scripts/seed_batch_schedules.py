import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from apps.batch.services.gpu.models_history import GpuPriceHistory
from shared.models.gpu_hardware import GpuManufacturer, GpuModel, GpuVariant, CpuManufacturer, CpuModel, CpuVariant
from shared.models.gpu_provider import Provider, ProviderRegion
from shared.models.gpu_offering import InstanceOffering, OfferingGpuConfiguration, OfferingCpuConfiguration, PricingPlan
from shared.models.retail import RtlPriceHistory
from apps.batch.services.financial.models import FinMktHistory
from shared.models.news import NewsArticle
from shared.models import *
from shared.db.session import AsyncSessionLocal
from shared.models.batch_schedule import SysBatSchBas, SysBatSchDtl

async def seed():
    async with AsyncSessionLocal() as session:
        try:
            # 1. BAS 삽입
            bas = SysBatSchBas(
                bat_id="GPU_DATA_CRAWLING",
                bat_nm="GPU Data Crawling",
                run_hr="0,8,16",
                run_min="0",
                run_sec="0",
                use_yn="Y"
            )
            session.add(bas)
            await session.commit()
            
            # 2. DTL 삽입
            providers = [
                "vast-ai", "runpod", "aws", "vessl", "xesktop",
                "gpuaas", "cloudv", "runyourai", "gabia", 
                "ktcloud", "sugarcube", "appleplaza", "ncloud", "rebellion"
            ]
            
            for i, slug in enumerate(providers):
                dtl = SysBatSchDtl(
                    bat_id="GPU_DATA_CRAWLING",
                    job_id=f"JOB_{slug.upper().replace('-', '_')}",
                    job_nm=f"{slug} Crawling",
                    exec_typ="SCRIPT",
                    exec_path="orchestrator.run_provider_collection",
                    run_ord=i + 1,
                    use_yn="Y",
                    ref_val_1=slug
                )
                session.add(dtl)
                
            await session.commit()
            print("Successfully seeded batch schedules!")
        except Exception as e:
            print(f"Error seeding batch schedules: {e}")
            await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed())
