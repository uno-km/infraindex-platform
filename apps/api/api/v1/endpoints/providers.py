from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.api.core.database import get_db
from apps.api.models.provider import Provider
from apps.api.schemas.provider import ProviderResponse, ProviderDetailResponse

router = APIRouter()

@router.get("/", response_model=List[ProviderResponse])
async def read_providers(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve providers.
    """
    result = await db.execute(select(Provider).offset(skip).limit(limit))
    providers = result.scalars().all()
    return providers

@router.get("/{provider_id}", response_model=ProviderDetailResponse)
async def read_provider(
    provider_id: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a specific provider by id.
    """
    result = await db.execute(select(Provider).where(Provider.id == provider_id))
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider
