from typing import Any
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from apps.api.core.limiter import limiter
from apps.api.core.database import get_db
from apps.api.models.offering import PricingPlan, InstanceOffering, OfferingGpuConfiguration
from apps.api.models.hardware import GpuVariant, GpuModel
from apps.api.schemas.search import SearchResponse
from apps.api.core.search.normalizer import QueryNormalizer
from apps.api.core.search.alias_resolver import AliasResolver

router = APIRouter()

@router.get("/gpus")
@limiter.limit("5/minute")
async def search_gpus(
    request: Request,
    q: str = Query(..., description="The search query (e.g. 'H100', '에이치백')"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Search for GPU rental offers using Advanced Search Engine.
    """
    # 1. Pipeline: Normalize & Resolve Alias
    norm_q = QueryNormalizer.normalize(q) if q else ""
    resolved_q = AliasResolver.resolve(norm_q)
    
    # 2. Base Query
    stmt = select(PricingPlan).options(
        selectinload(PricingPlan.offering).selectinload(InstanceOffering.provider),
        selectinload(PricingPlan.offering).selectinload(InstanceOffering.region),
        selectinload(PricingPlan.offering).selectinload(InstanceOffering.gpu_configuration).selectinload(OfferingGpuConfiguration.variant).selectinload(GpuVariant.model),
        selectinload(PricingPlan.observations)
    ).join(PricingPlan.offering).join(InstanceOffering.gpu_configuration).join(OfferingGpuConfiguration.variant).join(GpuVariant.model)
    
    # 3. Apply Fuzzy/Substring Filter
    if resolved_q:
        stmt = stmt.where(
            or_(
                GpuModel.name.ilike(f"%{resolved_q}%"),
                GpuVariant.name.ilike(f"%{resolved_q}%")
            )
        )
    
    result = await db.execute(stmt)
    plans = result.scalars().all()
    
    return SearchResponse(
        results=plans,
        total=len(plans),
        page=1,
        size=len(plans)
    )
