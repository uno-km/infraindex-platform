"""
apps/services/market/endpoints_retail_chart.py

Phase 1 — 리테일 OHLC 차트 API 엔드포인트
/api/v1/retail/chart/ohlc      - OHLC 시계열
/api/v1/retail/chart/summary   - 현재가 요약
/api/v1/retail/chart/products  - 상품 목록
/api/v1/retail/chart/backfill  - (관리자) 과거 데이터 집계
"""
import logging
from datetime import date, timedelta, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, desc

from apps.api.core.database import get_db
from apps.api.models.market import MarketProduct
from apps.api.models.ohlc import MarketOHLCDaily
from apps.services.market.ohlc_aggregator import (
    OHLCAggregator,
    ohlc_to_apexcharts,
    compute_summary,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def _timeframe_to_days(timeframe: str) -> int:
    """timeframe 문자열을 소급 일수로 변환"""
    mapping = {"1W": 7, "1M": 30, "3M": 90, "1Y": 365, "ALL": 3650}
    return mapping.get(timeframe.upper(), 30)


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/v1/retail/chart/products
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/chart/products")
async def list_retail_products(
    category: str | None = Query(None, description="GPU, CPU, RAM"),
    q: str | None = Query(None, description="검색어"),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, Any]]:
    """
    리테일 차트에서 선택 가능한 상품 목록 반환.
    tbl_market_ohlc_daily 에 최소 1건 이상 집계된 상품만 반환.
    """
    stmt = (
        select(MarketProduct)
        .join(MarketOHLCDaily, MarketOHLCDaily.product_id == MarketProduct.id)
        .distinct()
    )

    if category:
        stmt = stmt.where(MarketProduct.category == category.upper())
    if q:
        stmt = stmt.where(MarketProduct.model_name.ilike(f"%{q}%"))

    result = await db.execute(stmt)
    products = result.scalars().all()

    return [
        {
            "id": str(p.id),
            "manufacturer": p.manufacturer,
            "model_name": p.model_name,
            "category": p.category,
            "product_line": p.product_line,
        }
        for p in products
    ]


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/v1/retail/chart/ohlc
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/chart/ohlc")
async def get_retail_ohlc_chart(
    product_id: str = Query(..., description="MarketProduct UUID"),
    timeframe: str = Query("1M", description="1W|1M|3M|1Y|ALL"),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, Any]]:
    """
    리테일 상품의 일별 OHLC 캔들스틱 차트 데이터 반환.
    ApexCharts candlestick 형식: [{ x: "YYYY-MM-DD", o, h, l, c }, ...]
    """
    days = _timeframe_to_days(timeframe)
    from_date = date.today() - timedelta(days=days)

    stmt = (
        select(MarketOHLCDaily)
        .where(
            and_(
                MarketOHLCDaily.product_id == product_id,
                MarketOHLCDaily.trade_date >= from_date,
            )
        )
        .order_by(MarketOHLCDaily.trade_date)
    )

    result = await db.execute(stmt)
    rows = result.scalars().all()

    if not rows:
        return []

    return [
        ohlc_to_apexcharts(
            {
                "trade_date": row.trade_date,
                "open_price": row.open_price,
                "high_price": row.high_price,
                "low_price": row.low_price,
                "close_price": row.close_price,
            }
        )
        for row in rows
    ]


# ─────────────────────────────────────────────────────────────────────────────
# GET /api/v1/retail/chart/summary
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/chart/summary")
async def get_retail_summary(
    product_id: str = Query(..., description="MarketProduct UUID"),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    리테일 상품의 현재가, 등락폭, ATH/ATL 요약 반환.
    """
    # 최근 90일 데이터 기준
    from_date = date.today() - timedelta(days=90)

    stmt = (
        select(MarketOHLCDaily)
        .where(
            and_(
                MarketOHLCDaily.product_id == product_id,
                MarketOHLCDaily.trade_date >= from_date,
            )
        )
        .order_by(MarketOHLCDaily.trade_date)
    )

    result = await db.execute(stmt)
    rows = result.scalars().all()

    if not rows:
        return {
            "current_price": None,
            "change_1d": None,
            "change_pct_1d": None,
            "all_time_high": None,
            "all_time_low": None,
            "data_points": 0,
        }

    ohlc_dicts = [
        {
            "trade_date": r.trade_date,
            "open_price": r.open_price,
            "high_price": r.high_price,
            "low_price": r.low_price,
            "close_price": r.close_price,
        }
        for r in rows
    ]

    summary = compute_summary(ohlc_dicts)
    summary["data_points"] = len(rows)
    return summary


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/v1/retail/chart/aggregate  (관리자용: 수동 집계 트리거)
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/chart/aggregate")
async def trigger_ohlc_aggregation(
    target_date: date | None = None,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    OHLC 집계 수동 실행 (관리자용).
    target_date 미입력 시 어제 날짜로 실행.
    """
    if target_date is None:
        target_date = date.today() - timedelta(days=1)

    aggregator = OHLCAggregator()
    result = await aggregator.aggregate_daily(db, target_date)
    return {"status": "success", "target_date": str(target_date), **result}


# ─────────────────────────────────────────────────────────────────────────────
# POST /api/v1/retail/chart/backfill  (관리자용: 과거 데이터 전체 집계)
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/chart/backfill")
async def trigger_ohlc_backfill(
    from_date: date = Query(..., description="시작일 (YYYY-MM-DD)"),
    to_date: date = Query(..., description="종료일 (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    날짜 범위 전체 OHLC 백필 실행 (최초 실행 시 사용).
    주의: 대용량 데이터의 경우 수 분 소요.
    """
    if from_date > to_date:
        raise HTTPException(status_code=400, detail="from_date must be before to_date")

    aggregator = OHLCAggregator()
    result = await aggregator.backfill(db, from_date, to_date)
    return {"status": "success", **result}
