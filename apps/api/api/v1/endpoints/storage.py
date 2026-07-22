from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.api.core.database import get_db
from apps.api.models.storage import StorageTier
from apps.api.schemas.storage import StorageTierResponse

router = APIRouter()

@router.get("/", response_model=List[StorageTierResponse])
async def read_storage_tiers(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    result = await db.execute(select(StorageTier).offset(skip).limit(limit))
    return result.scalars().all()
