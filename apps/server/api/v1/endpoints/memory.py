from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from shared.db.session import get_db
from shared.models.memory import MemoryModule
from apps.server.schemas.memory import MemoryModuleResponse

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
