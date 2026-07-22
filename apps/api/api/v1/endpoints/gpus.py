from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from apps.api.core.database import get_db
from apps.api.models.hardware import GpuModel
from apps.api.schemas.gpu import GpuModelResponse

router = APIRouter()

@router.get("/", response_model=List[GpuModelResponse])
async def read_gpus(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve GPU models with their variants.
    """
    result = await db.execute(
        select(GpuModel)
        .options(selectinload(GpuModel.variants))
        .offset(skip)
        .limit(limit)
    )
    gpus = result.scalars().all()
    return gpus
