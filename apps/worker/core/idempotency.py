import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime, timezone
from apps.api.models.scheduler import IdempotencyKey

logger = logging.getLogger(__name__)

class LockAcquisitionError(Exception):
    pass

async def acquire_lock(db: AsyncSession, key: str, job_name: str) -> bool:
    """
    P1-002: 데이터베이스 트랜잭션을 이용한 분산 Idempotency 락.
    5분 단위 버킷을 키로 사용하여 동일한 수집 작업이 중복 실행되는 것을 방지합니다.
    """
    try:
        # 이미 락이 존재하는지 확인 (동일 버킷 내)
        result = await db.execute(select(IdempotencyKey).filter_by(key=key))
        existing = result.scalar_one_or_none()
        if existing:
            logger.info(f"Idempotency lock already exists for {key}")
            return False

        # 새 락 생성
        lock = IdempotencyKey(key=key, job_name=job_name)
        db.add(lock)
        await db.flush() # 트랜잭션 펜딩 (Unique 제약조건 충돌 체크)
        await db.commit()
        return True
    except IntegrityError:
        await db.rollback()
        return False
