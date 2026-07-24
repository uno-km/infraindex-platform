from typing import Any, List, Optional
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date, desc

from apps.api.core.database import get_db
from apps.services.gpu.models_history import GpuPriceHistory

router = APIRouter()


class PricePoint(BaseModel):
    timestamp: str
    price_per_hour: float
    availability_status: str


class PriceHistoryResponse(BaseModel):
    offering_id: str
    provider: str
    gpu_model: str
    vram_gb: float
    days_requested: int
    data_points: int
    history: List[PricePoint]


class PriceSummaryResponse(BaseModel):
    offering_id: str
    provider: str
    gpu_model: str
    period_days: int
    min_price: Optional[float]
    max_price: Optional[float]
    avg_price: Optional[float]
    latest_price: Optional[float]
    data_points: int


@router.get("/summary/{offering_id}", response_model=PriceSummaryResponse)
async def get_price_summary(
    offering_id: str,
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
) -> Any:
    provider, model_name, hw_type = _parse_offering_id(offering_id)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    result = await db.execute(
        select(
            func.min(GpuPriceHistory.prc_ph).label("min_price"),
            func.max(GpuPriceHistory.prc_ph).label("max_price"),
            func.avg(GpuPriceHistory.prc_ph).label("avg_price"),
            func.count(GpuPriceHistory.id).label("cnt"),
        )
        .where(_build_filter(PriceHistory, provider, model_name, hw_type))
        .where(GpuPriceHistory.ts >= since)
    )
    row = result.one_or_none()

    latest_result = await db.execute(
        select(GpuPriceHistory.prc_ph)
        .where(_build_filter(PriceHistory, provider, model_name, hw_type))
        .order_by(desc(GpuPriceHistory.ts))
        .limit(1)
    )
    latest_row = latest_result.scalar_one_or_none()

    return PriceSummaryResponse(
        offering_id=offering_id,
        provider=provider or "all",
        gpu_model=model_name, # schema field is gpu_model, we reuse it
        period_days=days,
        min_price=round(float(row.min_price), 4) if row and row.min_price is not None else None,
        max_price=round(float(row.max_price), 4) if row and row.max_price is not None else None,
        avg_price=round(float(row.avg_price), 4) if row and row.avg_price is not None else None,
        latest_price=round(float(latest_row), 4) if latest_row is not None else None,
        data_points=row.cnt if row else 0,
    )


@router.get("/{offering_id}", response_model=PriceHistoryResponse)
async def get_price_history(
    offering_id: str,
    days: int = Query(30, ge=1, le=365, description="조회 기간 (일)"),
    limit: int = Query(500, ge=1, le=2000, description="최대 반환 데이터 포인트 수"),
    db: AsyncSession = Depends(get_db),
) -> Any:
    provider, model_name, hw_type = _parse_offering_id(offering_id)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    query = (
        select(GpuPriceHistory)
        .where(_build_filter(GpuPriceHistory, provider, model_name, hw_type))
        .where(GpuPriceHistory.ts >= since)
        .order_by(GpuPriceHistory.ts.asc())
        .limit(limit)
    )

    result = await db.execute(query)
    rows = result.scalars().all()

    if not rows:
        return PriceHistoryResponse(
            offering_id=offering_id,
            provider=provider or "all",
            gpu_model=model_name,
            vram_gb=0.0,
            days_requested=days,
            data_points=0,
            history=[],
        )

    return PriceHistoryResponse(
        offering_id=offering_id,
        provider=rows[0].provider_id,
        gpu_model=rows[0].cpu_model if hw_type == "cpu" else rows[0].gpu_model,
        vram_gb=rows[0].vram_gb or 0.0,
        days_requested=days,
        data_points=len(rows),
        history=[
            PricePoint(
                timestamp=r.timestamp.isoformat(),
                price_per_hour=round(float(r.price_per_hour), 4),
                availability_status=r.availability_status,
            )
            for r in rows
        ],
    )


def _parse_offering_id(offering_id: str):
    """
    'vast-ai:H100' → ('vast-ai', 'H100', 'gpu')
    'cpu:vast-ai:EPYC' → ('vast-ai', 'EPYC', 'cpu')
    """
    hw_type = "gpu"
    if offering_id.startswith("cpu:"):
        hw_type = "cpu"
        offering_id = offering_id[4:]
    elif offering_id.startswith("gpu:"):
        hw_type = "gpu"
        offering_id = offering_id[4:]
        
    if ":" in offering_id:
        parts = offering_id.split(":", 1)
        return parts[0].strip(), parts[1].strip(), hw_type
    return None, offering_id.strip(), hw_type


def _build_filter(model, provider: Optional[str], target_model: str, hw_type: str = "gpu"):
    """공급자 + 모델 필터 조건 생성."""
    from sqlalchemy import and_
    if hw_type == "cpu":
        conditions = [model.cpu_model.ilike(f"%{target_model}%")]
    else:
        conditions = [model.gpu_model.ilike(f"%{target_model}%")]
        
    if provider:
        conditions.append(model.provider_id == provider)
    return and_(*conditions)
