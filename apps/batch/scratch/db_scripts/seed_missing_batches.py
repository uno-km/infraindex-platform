import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from shared.models.batch_schedule import SysBatSchBas, SysBatSchDtl
from shared.config.settings import settings

async def seed_missing():
    engine = create_async_engine(settings.async_database_uri, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)
    
    async with SessionLocal() as session:
        try:
            # RETAIL
            bas_retail = await session.get(SysBatSchBas, "RETAIL_DATA_CRAWLING")
            if not bas_retail:
                session.add(SysBatSchBas(bat_id="RETAIL_DATA_CRAWLING", bat_nm="Retail Data Crawling", run_hr="1", run_min="0", run_sec="0", use_yn="Y"))
                
            # FINANCIAL
            bas_fin = await session.get(SysBatSchBas, "FINANCIAL_DATA_CRAWLING")
            if not bas_fin:
                session.add(SysBatSchBas(bat_id="FINANCIAL_DATA_CRAWLING", bat_nm="Financial Data Crawling", run_hr="2", run_min="0", run_sec="0", use_yn="Y"))
                
            # NEWS
            bas_news = await session.get(SysBatSchBas, "NEWS_DATA_CRAWLING")
            if not bas_news:
                session.add(SysBatSchBas(bat_id="NEWS_DATA_CRAWLING", bat_nm="News Data Crawling", run_hr="3", run_min="0", run_sec="0", use_yn="Y"))
                
            await session.commit()
            
            # Retail DTLs
            retail_jobs = [("JOB_RETAIL_UNIVERSAL", "Universal Retail"), ("JOB_ENTERPRISE_HW", "Enterprise HW Retail")]
            for i, (jid, jnm) in enumerate(retail_jobs):
                if not await session.get(SysBatSchDtl, ("RETAIL_DATA_CRAWLING", jid)):
                    session.add(SysBatSchDtl(bat_id="RETAIL_DATA_CRAWLING", job_id=jid, job_nm=jnm, exec_typ="SCRIPT", exec_path="crawler_retail.run", run_ord=i+1, use_yn="Y", ref_val_1="retail"))
                    
            # Financial DTLs
            fin_jobs = [("JOB_STOCK_MARKET", "Stock Market"), ("JOB_DRAM_FUTURES", "DRAM Futures")]
            for i, (jid, jnm) in enumerate(fin_jobs):
                if not await session.get(SysBatSchDtl, ("FINANCIAL_DATA_CRAWLING", jid)):
                    session.add(SysBatSchDtl(bat_id="FINANCIAL_DATA_CRAWLING", job_id=jid, job_nm=jnm, exec_typ="SCRIPT", exec_path="crawler_financial.run", run_ord=i+1, use_yn="Y", ref_val_1="financial"))
                    
            # News DTLs
            if not await session.get(SysBatSchDtl, ("NEWS_DATA_CRAWLING", "JOB_NEWS_TIER")):
                session.add(SysBatSchDtl(bat_id="NEWS_DATA_CRAWLING", job_id="JOB_NEWS_TIER", job_nm="News Tier Crawling", exec_typ="SCRIPT", exec_path="crawler_news.run", run_ord=1, use_yn="Y", ref_val_1="news"))
                
            await session.commit()
            print("Successfully seeded missing batch schedules!")
        except Exception as e:
            print(f"Error seeding missing batch schedules: {e}")
            await session.rollback()
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed_missing())
