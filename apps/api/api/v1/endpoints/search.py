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


def _is_quarantined(plan: PricingPlan) -> bool:
    """
    P2-003: Search quarantine filter.
    격리된 가격 플랜을 검색 결과에서 제외.

    판단 기준:
    1. 연결된 관측값(observations)이 없는 경우 — 데이터 없음
    2. 가장 최근 관측값의 가격이 0 이하인 경우 — 이상 데이터
    3. 가장 최근 관측값의 가격이 $1,000/hr 초과인 경우 — 극단적 이상치
    """
    observations = getattr(plan, "observations", None)
    if not observations:
        return True  # 관측값 없음 → 격리

    # 가장 최근 관측값으로 판단
    latest = max(observations, key=lambda o: o.observed_at, default=None)
    if latest is None:
        return True

    try:
        price = float(latest.price_per_hour)
    except (TypeError, ValueError):
        return True  # 가격 파싱 불가 → 격리

    if price <= 0:
        return True
    if price > 1000.0:
        return True

    return False


@router.get("/gpus")
@limiter.limit("5/minute")
async def search_gpus(
    request: Request,
    q: str = Query(..., description="The search query (e.g. 'H100', '에이치백')"),
    include_quarantined: bool = Query(False, description="격리된 항목도 포함 (관리자용)"),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Search for GPU rental offers using Advanced Search Engine.

    P2-003: Quarantine filter 적용.
    가격 이상치·데이터 없는 플랜은 기본적으로 결과에서 제외됨.
    include_quarantined=true 파라미터로 전체 조회 가능 (관리자 디버깅용).
    """
    # 1. Pipeline: Normalize & Resolve Alias
    norm_q = QueryNormalizer.normalize(q) if q else ""
    resolved_q = AliasResolver.resolve(norm_q)

    # 2. Base Query
    stmt = select(PricingPlan).options(
        selectinload(PricingPlan.offering).selectinload(InstanceOffering.provider),
        selectinload(PricingPlan.offering).selectinload(InstanceOffering.region),
        selectinload(PricingPlan.offering).selectinload(
            InstanceOffering.gpu_configuration
        ).selectinload(OfferingGpuConfiguration.variant).selectinload(GpuVariant.model),
        selectinload(PricingPlan.observations),
    ).join(PricingPlan.offering).join(
        InstanceOffering.gpu_configuration
    ).join(OfferingGpuConfiguration.variant).join(GpuVariant.model)

    # 3. Apply Fuzzy/Substring Filter
    if resolved_q:
        stmt = stmt.where(
            or_(
                GpuModel.name.ilike(f"%{resolved_q}%"),
                GpuVariant.name.ilike(f"%{resolved_q}%"),
            )
        )

    result = await db.execute(stmt)
    plans = result.scalars().all()

    # 4. P2-003: Quarantine Filter — 이상치 제거
    if not include_quarantined:
        original_count = len(plans)
        plans = [p for p in plans if not _is_quarantined(p)]
        filtered_count = original_count - len(plans)
        if filtered_count > 0:
            import logging
            logging.getLogger(__name__).info(
                f"[Search] Quarantine filter removed {filtered_count}/{original_count} "
                f"plans for query='{q}'"
            )

    return SearchResponse(
        results=plans,
        total=len(plans),
        page=1,
        size=len(plans),
    )
