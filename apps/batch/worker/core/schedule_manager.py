import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from apps.batch.worker.core.config import settings
from shared.models.batch_schedule import SysBatSchBas

logger = logging.getLogger(__name__)

class BatchScheduleManager:
    _instance: Optional['BatchScheduleManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BatchScheduleManager, cls).__new__(cls)
            cls._instance._schedules = {}
            cls._instance._is_loaded = False
        return cls._instance

    async def load_schedules(self) -> None:
        """
        DB에서 SYS_BAT_SCH_BAS 테이블을 싹 긁어서 메모리(Singleton)에 적재합니다.
        """
        if not settings.USE_REAL_DB or not settings.DATABASE_URL:
            logger.warning("[ScheduleManager] DB 미사용 설정 — 스케줄 적재 생략.")
            return

        logger.info("[ScheduleManager] 마스터 배치 스케줄(BAS) DB에서 로드 중...")
        try:
            db_url = settings.DATABASE_URL
            if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
                db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

            engine = create_async_engine(db_url, echo=False, future=True, pool_size=2, max_overflow=5)
            SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

            async with SessionLocal() as session:
                stmt = select(SysBatSchBas).where(SysBatSchBas.use_yn == "Y")
                result = await session.execute(stmt)
                records = result.scalars().all()

                new_schedules = {}
                for r in records:
                    new_schedules[r.bat_id] = {
                        "bat_id": r.bat_id,
                        "bat_nm": r.bat_nm,
                        "run_hr": [int(x.strip()) for x in r.run_hr.split(",")] if r.run_hr else [],
                        "run_min": [int(x.strip()) for x in r.run_min.split(",")] if r.run_min else [0],
                    }
                
                self._schedules = new_schedules
                self._is_loaded = True
                logger.info(f"[ScheduleManager] 스케줄 적재 완료: {list(new_schedules.keys())}")

            await engine.dispose()
        except Exception as e:
            logger.error(f"[ScheduleManager] 스케줄 로드 실패: {e}")

    def get_schedules(self) -> Dict[str, Any]:
        return self._schedules

    def is_time_to_run(self, bat_id: str) -> bool:
        """
        현재 시간이 해당 배치의 실행 조건에 맞는지 확인합니다.
        """
        sched = self._schedules.get(bat_id)
        if not sched:
            return False
            
        now = datetime.now()
        # 한국시간 KST 기준(UTC+9)으로 스케줄링 한다고 가정할 때, 
        # 서버시간이 이미 KST로 설정되어 있다면 now.hour 그대로 사용
        # (Dockerfile에서 TZ=Asia/Seoul 설정을 주로 사용하므로 그대로 적용)
        
        match_hr = now.hour in sched["run_hr"] if sched["run_hr"] else True
        match_min = now.minute in sched["run_min"] if sched["run_min"] else True
        
        return match_hr and match_min

    def load_sync(self):
        """동기적으로 스케줄을 로드합니다. 워커 부트스트랩 시 사용."""
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.ensure_future(self.load_schedules())
        else:
            loop.run_until_complete(self.load_schedules())


schedule_manager = BatchScheduleManager()
