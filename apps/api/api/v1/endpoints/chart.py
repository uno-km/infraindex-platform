from typing import Any, List, Optional
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date, or_

from apps.api.core.database import get_db
from apps.services.gpu.models_history import GpuPriceHistory
from apps.api.models.storage import StoragePriceHistory

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
    model_name: str
    provider: str
    data: List[ChartDataPoint]


from fastapi_cache.decorator import cache

@router.get("/candlestick", response_model=List[CandlestickDataPoint])
@cache(expire=3600 * 8)
async def get_candlestick(
    gpu_model_id: str = Query(..., description="GPU model name"),
    days: int = Query(90, description="Number of days"),
    db: AsyncSession = Depends(get_db),
):
    import datetime as dt
    since = datetime.now(timezone.utc) - dt.timedelta(days=days)
    
    query = (
        select(GpuPriceHistory)
        .where(
            or_(
                GpuPriceHistory.gpu_mdl.ilike(f"%{gpu_model_id}%"),
                GpuPriceHistory.cpu_mdl.ilike(f"%{gpu_model_id}%")
            )
        )
        .where(GpuPriceHistory.ts >= since)
        .order_by(GpuPriceHistory.ts.asc())
    )
    if db is not None:
        result = await db.execute(query)
        rows = result.scalars().all()
    else:
        rows = []
    
    if not rows:
        # Fallback to all historical JSON files if DB is empty
        from apps.api.core.data_service import DataService
        records = await DataService.get_all_historical_prices()
        
        target = DataService._normalize_gpu_name(gpu_model_id).lower()
        
        filtered = []
        for r in records:
            raw_name = r.get("gpu_model") or r.get("gpu_name") or r.get("cpu_model") or r.get("name") or r.get("instance_type") or ""
            norm_name = DataService._normalize_gpu_name(raw_name).lower()
            if target and norm_name and (target in norm_name or norm_name in target):
                filtered.append(r)
        
        if not filtered:
            return []

        # Group by actual collected date (YYYY-MM-DD)
        daily_json_groups = defaultdict(list)
        for r in filtered:
            dt = r.get("timestamp")
            if dt:
                day_str = dt.strftime("%Y-%m-%d")
            else:
                day_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            daily_json_groups[day_str].append(r)

        candlesticks = []
        for day_str in sorted(daily_json_groups.keys()):
            day_records = [r for r in daily_json_groups[day_str] if r.get("price_per_hour") and r.get("price_per_hour") > 0]
            if not day_records:
                continue

            day_records.sort(key=lambda r: r.get("timestamp") or datetime.now(timezone.utc))
            prices = [float(r["price_per_hour"]) for r in day_records]
            if not prices:
                continue

            sorted_by_price = sorted(day_records, key=lambda r: r["price_per_hour"])
            low_record = sorted_by_price[0]
            high_record = sorted_by_price[-1]
            
            avg_price = sum(prices) / len(prices)
            half = max(1, len(prices) // 3)
            open_price = sum(prices[:half]) / half
            close_price = sum(prices[-half:]) / len(prices[-half:])

            if abs(open_price - close_price) < 0.001:
                open_price = round(float(avg_price) * 0.99, 4)
                close_price = round(float(avg_price) * 1.01, 4)

            candlesticks.append(CandlestickDataPoint(
                x=day_str + "T00:00:00Z",
                y=[round(float(open_price), 4), round(float(high_record["price_per_hour"]), 4), round(float(low_record["price_per_hour"]), 4), round(float(close_price), 4)],
                highProvider=high_record.get("provider", "unknown"),
                lowProvider=low_record.get("provider", "unknown"),
                avg=round(float(avg_price), 4)
            ))
    else:
        # Group by day
        daily_groups = defaultdict(list)
        for row in rows:
            day_str = row.ts.strftime("%Y-%m-%d") if row.ts else datetime.now(timezone.utc).strftime("%Y-%m-%d")
            daily_groups[day_str].append(row)
            
        candlesticks = []
        for day_str in sorted(daily_groups.keys()):
            records = daily_groups[day_str]
            records.sort(key=lambda r: r.ts or datetime.now(timezone.utc))
            
            first_third = max(1, len(records) // 3)
            last_third = max(1, len(records) // 3)
            
            open_price = sum(float(r.prc_ph) for r in records[:first_third] if r.prc_ph) / first_third
            close_price = sum(float(r.prc_ph) for r in records[-last_third:] if r.prc_ph) / last_third
            
            sorted_by_price = sorted([r for r in records if r.prc_ph], key=lambda r: float(r.prc_ph))
            if not sorted_by_price:
                continue
            low_record = sorted_by_price[0]
            high_record = sorted_by_price[-1]
            
            avg_price = sum(float(r.prc_ph) for r in sorted_by_price) / len(sorted_by_price)
            
            if abs(open_price - close_price) < 0.001:
                open_price = avg_price * 0.99
                close_price = avg_price * 1.01
            
            candlesticks.append(CandlestickDataPoint(
                x=day_str + "T00:00:00Z",
                y=[round(open_price, 4), round(float(high_record.prc_ph), 4), round(float(low_record.prc_ph), 4), round(close_price, 4)],
                highProvider=high_record.prv_id,
                lowProvider=low_record.prv_id,
                avg=round(avg_price, 4)
            ))

    return candlesticks

@router.get("/price-series", response_model=List[ChartSeriesResponse])
@cache(expire=3600 * 8)
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
    import datetime as dt
    since = datetime.now(timezone.utc) - dt.timedelta(days=days)

    # 일별 집계 쿼리
    day_col = cast(GpuPriceHistory.ts, Date).label("day")
    query = (
        select(
            GpuPriceHistory.gpu_mdl,
            GpuPriceHistory.prv_id,
            day_col,
            func.min(GpuPriceHistory.prc_ph).label("min_price"),
            func.max(GpuPriceHistory.prc_ph).label("max_price"),
            func.avg(GpuPriceHistory.prc_ph).label("avg_price"),
            func.count(GpuPriceHistory.id).label("cnt"),
        )
        .where(GpuPriceHistory.gpu_mdl.ilike(f"%{gpu_model_id}%"))
        .where(GpuPriceHistory.ts >= since)
        .group_by(GpuPriceHistory.gpu_mdl, GpuPriceHistory.prv_id, day_col)
        .order_by(GpuPriceHistory.prv_id, day_col)
    )

    if provider:
        query = query.where(GpuPriceHistory.prv_id == provider)

    if db is not None:
        result = await db.execute(query)
        rows = result.all()
    else:
        rows = []

    if not rows:
        return []

    # provider별로 그루핑
    series_map: dict = {}
    for row in rows:
        key = (row.gpu_mdl, row.prv_id)
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
            model_name=gpu,
            provider=prov,
            data=points,
        )
        for (gpu, prov), points in series_map.items()
    ]


@router.get("/cpu-price-series", response_model=List[ChartSeriesResponse])
@cache(expire=3600 * 8)
async def get_cpu_price_series(
    cpu_model_id: str = Query(..., description="CPU model name (e.g. 'EPYC', 'Xeon')"),
    provider: Optional[str] = Query(None, description="Filter by provider slug"),
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
) -> Any:
    import datetime as dt
    since = datetime.now(timezone.utc) - dt.timedelta(days=days)

    day_col = cast(GpuPriceHistory.ts, Date).label("day")
    query = (
        select(
            GpuPriceHistory.cpu_mdl,
            GpuPriceHistory.prv_id,
            day_col,
            func.min(GpuPriceHistory.prc_ph).label("min_price"),
            func.max(GpuPriceHistory.prc_ph).label("max_price"),
            func.avg(GpuPriceHistory.prc_ph).label("avg_price"),
            func.count(GpuPriceHistory.id).label("cnt"),
        )
        .where(GpuPriceHistory.hw_typ == "cpu")
        .where(GpuPriceHistory.cpu_mdl.ilike(f"%{cpu_model_id}%"))
        .where(GpuPriceHistory.ts >= since)
        .group_by(GpuPriceHistory.cpu_mdl, GpuPriceHistory.prv_id, day_col)
        .order_by(GpuPriceHistory.prv_id, day_col)
    )

    if provider:
        query = query.where(GpuPriceHistory.prv_id == provider)

    if db is not None:
        result = await db.execute(query)
        rows = result.all()
    else:
        rows = []

    if not rows:
        return []

    series_map: dict = {}
    for row in rows:
        key = (row.cpu_mdl, row.prv_id)
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
            model_name=cpu or "Unknown",
            provider=prov,
            data=points,
        )
        for (cpu, prov), points in series_map.items()
    ]
@router.get("/unified-price-series", response_model=List[ChartSeriesResponse])
@cache(expire=3600 * 8)
async def get_unified_price_series(
    hw_typ: str = Query("gpu", description="Hardware type (e.g., 'gpu', 'cpu', 'storage', 'baremetal')"),
    model_id: str = Query(..., description="Model ID or identifier (e.g., 'H100', 'EPYC', 'S3 Standard')"),
    provider: Optional[str] = Query(None, description="Filter by provider slug"),
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
) -> Any:
    import datetime as dt
    since = datetime.now(timezone.utc) - dt.timedelta(days=days)
    hw_typ = hw_typ.lower()

    if hw_typ == "storage":
        day_col = cast(StoragePriceHistory.ts, Date).label("day")
        query = (
            select(
                StoragePriceHistory.storage_mdl.label("model_name"),
                StoragePriceHistory.prv_id,
                day_col,
                func.min(StoragePriceHistory.prc_pgb_mth).label("min_price"),
                func.max(StoragePriceHistory.prc_pgb_mth).label("max_price"),
                func.avg(StoragePriceHistory.prc_pgb_mth).label("avg_price"),
                func.count(StoragePriceHistory.id).label("cnt"),
            )
            .where(StoragePriceHistory.storage_mdl.ilike(f"%{model_id}%"))
            .where(StoragePriceHistory.ts >= since)
            .group_by(StoragePriceHistory.storage_mdl, StoragePriceHistory.prv_id, day_col)
            .order_by(StoragePriceHistory.prv_id, day_col)
        )
        if provider:
            query = query.where(StoragePriceHistory.prv_id == provider)
    else:
        # Default to GpuPriceHistory for gpu, cpu, baremetal
        day_col = cast(GpuPriceHistory.ts, Date).label("day")
        
        # Decide which model column to search based on hw_typ
        if hw_typ == "gpu":
            model_col = GpuPriceHistory.gpu_mdl
        elif hw_typ == "cpu":
            model_col = GpuPriceHistory.cpu_mdl
        elif hw_typ == "baremetal":
            model_col = GpuPriceHistory.cpu_mdl # Re-using cpu_mdl for baremetal model string
        else:
            model_col = GpuPriceHistory.gpu_mdl # default fallback

        query = (
            select(
                model_col.label("model_name"),
                GpuPriceHistory.prv_id,
                day_col,
                func.min(GpuPriceHistory.prc_ph).label("min_price"),
                func.max(GpuPriceHistory.prc_ph).label("max_price"),
                func.avg(GpuPriceHistory.prc_ph).label("avg_price"),
                func.count(GpuPriceHistory.id).label("cnt"),
            )
            .where(GpuPriceHistory.hw_typ == hw_typ)
            .where(model_col.ilike(f"%{model_id}%"))
            .where(GpuPriceHistory.ts >= since)
            .group_by(model_col, GpuPriceHistory.prv_id, day_col)
            .order_by(GpuPriceHistory.prv_id, day_col)
        )
        if provider:
            query = query.where(GpuPriceHistory.prv_id == provider)

    if db is not None:
        result = await db.execute(query)
        rows = result.all()
    else:
        rows = []

    if not rows:
        return []

    series_map: dict = {}
    for row in rows:
        key = (row.model_name, row.prv_id)
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
            model_name=m_name or "Unknown",
            provider=prov,
            data=points,
        )
        for (m_name, prov), points in series_map.items()
    ]


@router.post("/storage/sync-global", summary="전세계 스토리지 가격 동기화")
async def sync_global_storage_prices(
    db: AsyncSession = Depends(get_db),
):
    """
    전세계 18개 스토리지 공급자(AWS/GCP/Azure/Cloudflare/Backblaze 등 + 국내)
    공개 가격을 수집하여 DB에 저장합니다.
    실시간 환율(USD/KRW)을 적용합니다.
    """
    if db is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Database not available")

    from apps.services.market.crawler_storage_global import GlobalStorageCrawler
    crawler = GlobalStorageCrawler()
    result = await crawler.sync_to_db(db)
    return result


@router.get("/storage/providers", summary="수집된 스토리지 공급자 목록")
async def list_storage_providers(
    db: AsyncSession = Depends(get_db),
):
    """StoragePriceHistory에 저장된 공급자 + 제품 목록 반환"""
    if db is None:
        return []

    from sqlalchemy import distinct
    stmt = (
        select(
            distinct(StoragePriceHistory.prv_id).label("provider"),
            StoragePriceHistory.storage_mdl.label("product"),
        )
        .order_by(StoragePriceHistory.prv_id)
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [{"provider": r.provider, "product": r.product} for r in rows]

