import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from shared.models.batch_schedule import SysBatSchDtl, SysBatSchHist
from shared.config.settings import settings

async def main():
    engine = create_async_engine(settings.async_database_uri, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)
    
    async with SessionLocal() as session:
        result = await session.execute(select(SysBatSchDtl).where(SysBatSchDtl.use_yn == 'Y'))
        dtls = result.scalars().all()
        print("=== 📌 현재 DB에 등록된 활성 배치 잡 목록 (USE_YN='Y') ===")
        print(f"총 {len(dtls)}개의 잡이 대기 중입니다:")
        for idx, d in enumerate(dtls, 1):
            print(f"  {idx}. [{d.bat_id}] {d.job_id} (Provider: {d.ref_val_1})")
            
        print("\n=== 📝 최근 배치 실행 히스토리 (SYS_BAT_SCH_HIST) ===")
        hist_result = await session.execute(select(SysBatSchHist).order_by(SysBatSchHist.seq.desc()).limit(15))
        hists = hist_result.scalars().all()
        for h in hists:
            print(f"  - {h.bat_id} / {h.job_id} | Status: {h.status} | {h.start_dt} ~ {h.end_dt}")
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
