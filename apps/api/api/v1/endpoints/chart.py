from typing import Any, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.core.database import get_db

router = APIRouter()

class ChartDataPoint(BaseModel):
    timestamp: str
    min_price: float
    max_price: float
    avg_price: float

class ChartSeriesResponse(BaseModel):
    gpu_model: str
    provider: str
    data: List[ChartDataPoint]

@router.get("/price-series", response_model=List[ChartSeriesResponse])
async def get_price_series(
    gpu_model_id: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Time-Series API for Charting.
    Returns aggregated price points (min, max, avg) for a given GPU over time.
    (Phase 9 Scaffold - Returns mocked downsampled data for UI verification)
    """
    # In production, this uses TimescaleDB hypertable queries or continuous aggregates.
    # Returning a scaffolded response to verify the frontend ECharts/Lightweight charts integration.
    return [
        ChartSeriesResponse(
            gpu_model="H100",
            provider="Vast.ai",
            data=[
                ChartDataPoint(timestamp="2026-07-20T09:00:00Z", min_price=1.85, max_price=2.10, avg_price=1.95),
                ChartDataPoint(timestamp="2026-07-21T09:00:00Z", min_price=1.90, max_price=2.20, avg_price=2.05),
                ChartDataPoint(timestamp="2026-07-22T09:00:00Z", min_price=1.88, max_price=2.15, avg_price=2.00),
            ]
        )
    ]
