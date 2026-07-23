from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.api.core.database import get_db
from apps.api.models.memory import MemoryModule
from apps.api.schemas.memory import MemoryModuleResponse

router = APIRouter()

@router.get("/", response_model=List[MemoryModuleResponse])
async def read_memory_modules(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    if db is None:
        return []
    result = await db.execute(select(MemoryModule).offset(skip).limit(limit))
    return result.scalars().all()
