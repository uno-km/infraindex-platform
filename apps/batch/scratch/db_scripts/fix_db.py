import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import update
from shared.models.batch_schedule import SysBatSchDtl
from shared.config.settings import settings

async def fix():
    engine = create_async_engine(settings.async_database_uri, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)
    async with SessionLocal() as session:
        await session.execute(update(SysBatSchDtl).where(SysBatSchDtl.job_id == 'JOB_RETAIL_UNIVERSAL').values(ref_val_1='naver'))
        await session.execute(update(SysBatSchDtl).where(SysBatSchDtl.job_id == 'JOB_ENTERPRISE_HW').values(ref_val_1='coupang'))
        await session.commit()
        print("Fixed retail refs to naver and coupang")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(fix())
