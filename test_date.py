import os
os.environ['USE_REAL_DB'] = 'True'
import asyncio
from sqlalchemy import select
from apps.api.core.database import AsyncSessionLocal
from apps.services.gpu.models_history import GpuPriceHistory

async def main():
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(GpuPriceHistory.ts, GpuPriceHistory.gpu_mdl).limit(100))
        dates = set(row[0].date() for row in res.all())
        print("Dates in DB:", dates)

asyncio.run(main())
