from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime, timezone
from apps.api.models.scheduler import IdempotencyKey

class LockAcquisitionError(Exception):
    pass

async def acquire_lock(db: AsyncSession, key: str, job_name: str) -> bool:
    """
    Attempts to acquire a distributed lock for a given key.
    Uses PostgreSQL unique constraint on 'key' to guarantee idempotency.
    Returns True if lock acquired (meaning it's safe to run), False otherwise.
    """
    try:
        lock = IdempotencyKey(
            key=key,
            job_name=job_name,
            executed_at=datetime.now(timezone.utc)
        )
        db.add(lock)
        await db.commit()
        return True
    except IntegrityError:
        await db.rollback()
        return False
