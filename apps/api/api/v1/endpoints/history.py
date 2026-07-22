from typing import Any, List, Optional
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date, desc

from apps.api.core.database import get_db
from apps.api.models.history import PriceHistory

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
    """
    P1-005: GPU 가격 요약 통계 (offering_id = provider_slug:gpu_model 형식).
    예: /api/v1/history/summary/vast-ai:H100?days=7
    """
    provider, gpu_model = _parse_offering_id(offering_id)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    result = await db.execute(
        select(
            func.min(PriceHistory.price_per_hour).label("min_price"),
            func.max(PriceHistory.price_per_hour).label("max_price"),
            func.avg(PriceHistory.price_per_hour).label("avg_price"),
            func.count(PriceHistory.id).label("cnt"),
        )
        .where(_build_filter(PriceHistory, provider, gpu_model))
        .where(PriceHistory.timestamp >= since)
    )
    row = result.one_or_none()

    # 가장 최근 가격
    latest_result = await db.execute(
        select(PriceHistory.price_per_hour)
        .where(_build_filter(PriceHistory, provider, gpu_model))
        .order_by(desc(PriceHistory.timestamp))
        .limit(1)
    )
    latest_row = latest_result.scalar_one_or_none()

    return PriceSummaryResponse(
        offering_id=offering_id,
        provider=provider or "all",
        gpu_model=gpu_model,
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
    """
    P1-005: GET /api/v1/history/{offering_id}
    offering_id 형식: <provider_slug>:<gpu_model>
    예: vast-ai:H100, runpod:RTX%204090

    price_history 테이블에서 실제 데이터를 반환.
    데이터 없으면 빈 history 반환 (가짜 데이터 없음).
    """
    provider, gpu_model = _parse_offering_id(offering_id)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    query = (
        select(PriceHistory)
        .where(_build_filter(PriceHistory, provider, gpu_model))
        .where(PriceHistory.timestamp >= since)
        .order_by(PriceHistory.timestamp.asc())
        .limit(limit)
    )

    result = await db.execute(query)
    rows = result.scalars().all()

    if not rows:
        return PriceHistoryResponse(
            offering_id=offering_id,
            provider=provider or "all",
            gpu_model=gpu_model,
            vram_gb=0.0,
            days_requested=days,
            data_points=0,
            history=[],
        )

    return PriceHistoryResponse(
        offering_id=offering_id,
        provider=rows[0].provider_id,
        gpu_model=rows[0].gpu_model,
        vram_gb=rows[0].vram_gb,
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
    'vast-ai:H100' → ('vast-ai', 'H100')
    'H100'          → (None, 'H100')  — provider 미지정 = 전체 공급자
    """
    if ":" in offering_id:
        parts = offering_id.split(":", 1)
        return parts[0].strip(), parts[1].strip()
    return None, offering_id.strip()


def _build_filter(model, provider: Optional[str], gpu_model: str):
    """공급자 + GPU 모델 필터 조건 생성."""
    from sqlalchemy import and_
    conditions = [model.gpu_model.ilike(f"%{gpu_model}%")]
    if provider:
        conditions.append(model.provider_id == provider)
    return and_(*conditions)
