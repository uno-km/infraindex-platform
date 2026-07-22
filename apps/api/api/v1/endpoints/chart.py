from typing import Any, List, Optional
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date

from apps.api.core.database import get_db
from apps.api.models.history import PriceHistory

from collections import defaultdict

router = APIRouter()


class CandlestickDataPoint(BaseModel):
    x: str
    y: List[float]  # [open, high, low, close]
    highProvider: str
    lowProvider: str
    avg: float

class ChartDataPoint(BaseModel):
    timestamp: str
    min_price: float
    max_price: float
    avg_price: float
    data_point_count: int


class ChartSeriesResponse(BaseModel):
    gpu_model: str
    provider: str
    data: List[ChartDataPoint]


@router.get("/candlestick", response_model=List[CandlestickDataPoint])
async def get_candlestick(
    gpu_model_id: str = Query(..., description="GPU model name"),
    days: int = Query(90, description="Number of days"),
    db: AsyncSession = Depends(get_db),
):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    
    query = (
        select(PriceHistory)
        .where(PriceHistory.gpu_model.ilike(f"%{gpu_model_id}%"))
        .where(PriceHistory.timestamp >= since)
        .order_by(PriceHistory.timestamp.asc())
    )
    result = await db.execute(query)
    rows = result.scalars().all()
    
    if not rows:
        # Fallback to local JSON files if DB is empty
        from apps.api.core.data_service import DataService
        records = await DataService.get_latest_prices()
        
        # We need to apply the same normalization
        target = DataService._normalize_gpu_name(gpu_model_id).lower()
        
        filtered = []
        for r in records:
            raw_name = r.get("gpu_model") or r.get("gpu_name") or ""
            norm_name = DataService._normalize_gpu_name(raw_name).lower()
            if target in norm_name or norm_name in target:
                filtered.append(r)
        
        if not filtered:
            return []
            
        open_price = sum(r["price_per_hour"] for r in filtered) / len(filtered)
        close_price = sum(r["price_per_hour"] for r in filtered) / len(filtered)
        
        sorted_by_price = sorted(filtered, key=lambda r: r["price_per_hour"])
        low_record = sorted_by_price[0]
        high_record = sorted_by_price[-1]
        avg_price = sum(r["price_per_hour"] for r in filtered) / len(filtered)
        
        return [CandlestickDataPoint(
            x=datetime.now(timezone.utc).strftime("%Y-%m-%d") + "T00:00:00Z",
            y=[round(open_price, 4), round(high_record["price_per_hour"], 4), round(low_record["price_per_hour"], 4), round(close_price, 4)],
            highProvider=high_record["provider"],
            lowProvider=low_record["provider"],
            avg=round(avg_price, 4)
        )]
        
    # Group by day
    daily_groups = defaultdict(list)
    for row in rows:
        day_str = row.timestamp.strftime("%Y-%m-%d")
        daily_groups[day_str].append(row)
        
    candlesticks = []
    for day_str, records in daily_groups.items():
        records.sort(key=lambda r: r.timestamp)
        open_price = sum(r.price_per_hour for r in records[:max(1, len(records)//3)]) / max(1, len(records[:max(1, len(records)//3)]))
        close_price = sum(r.price_per_hour for r in records[-max(1, len(records)//3):]) / max(1, len(records[-max(1, len(records)//3):]))
        
        sorted_by_price = sorted(records, key=lambda r: r.price_per_hour)
        low_record = sorted_by_price[0]
        high_record = sorted_by_price[-1]
        
        avg_price = sum(r.price_per_hour for r in records) / len(records)
        
        candlesticks.append(CandlestickDataPoint(
            x=day_str + "T00:00:00Z",
            y=[round(open_price, 4), round(high_record.price_per_hour, 4), round(low_record.price_per_hour, 4), round(close_price, 4)],
            highProvider=high_record.provider_id,
            lowProvider=low_record.provider_id,
            avg=round(avg_price, 4)
        ))
        
    return candlesticks

@router.get("/price-series", response_model=List[ChartSeriesResponse])
async def get_price_series(
    gpu_model_id: str = Query(..., description="GPU model name (e.g. 'H100', 'RTX 4090')"),
    provider: Optional[str] = Query(None, description="Filter by provider slug (e.g. 'vast-ai', 'runpod')"),
    days: int = Query(30, ge=1, le=365, description="Number of days of history to return"),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    FIX-08: Time-Series API — 실제 DB price_history 테이블 조회.

    - gpu_model_id로 ILIKE 검색 (대소문자 무관)
    - 일별 집계: MIN/MAX/AVG price_per_hour
    - provider 파라미터로 공급자 필터 가능
    - days 파라미터로 조회 기간 조정 (기본 30일)

    price_history 테이블에 데이터가 없으면 빈 배열 반환.
    (가짜 Mock 데이터를 절대 반환하지 않음)
    """
    since = datetime.now(timezone.utc) - timedelta(days=days)

    # 일별 집계 쿼리
    day_col = cast(PriceHistory.timestamp, Date).label("day")
    query = (
        select(
            PriceHistory.gpu_model,
            PriceHistory.provider_id,
            day_col,
            func.min(PriceHistory.price_per_hour).label("min_price"),
            func.max(PriceHistory.price_per_hour).label("max_price"),
            func.avg(PriceHistory.price_per_hour).label("avg_price"),
            func.count(PriceHistory.id).label("cnt"),
        )
        .where(PriceHistory.gpu_model.ilike(f"%{gpu_model_id}%"))
        .where(PriceHistory.timestamp >= since)
        .group_by(PriceHistory.gpu_model, PriceHistory.provider_id, day_col)
        .order_by(PriceHistory.provider_id, day_col)
    )

    if provider:
        query = query.where(PriceHistory.provider_id == provider)

    result = await db.execute(query)
    rows = result.all()

    if not rows:
        return []

    # provider별로 그루핑
    series_map: dict = {}
    for row in rows:
        key = (row.gpu_model, row.provider_id)
        if key not in series_map:
            series_map[key] = []
        series_map[key].append(
            ChartDataPoint(
                timestamp=row.day.isoformat() + "T00:00:00Z",
                min_price=round(float(row.min_price), 4),
                max_price=round(float(row.max_price), 4),
                avg_price=round(float(row.avg_price), 4),
                data_point_count=row.cnt,
            )
        )

    return [
        ChartSeriesResponse(
            gpu_model=gpu,
            provider=prov,
            data=points,
        )
        for (gpu, prov), points in series_map.items()
    ]
