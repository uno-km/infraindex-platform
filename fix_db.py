import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import update
from apps.api.models.batch_schedule import SysBatSchDtl
from apps.api.core.config import settings

async def fix():
    engine = create_async_engine(settings.async_database_uri, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)
    async with SessionLocal() as session:
        await session.execute(update(SysBatSchDtl).where(SysBatSchDtl.job_id == 'JOB_STOCK_MARKET').values(ref_val_1='stock_market'))
        await session.execute(update(SysBatSchDtl).where(SysBatSchDtl.job_id == 'JOB_DRAM_FUTURES').values(ref_val_1='dram_futures'))
        await session.commit()
        print("Fixed financial ref_val_1 again")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(fix())
