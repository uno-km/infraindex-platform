from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc
from typing import List, Dict, Any
from datetime import datetime, timedelta

from apps.api.core.database import get_db

router = APIRouter()

@router.get("/ohlc")
async def get_retail_ohlc(
    hardware_type: str = Query(..., description="gpu, cpu, or ram"),
    model_name: str = Query(..., description="Exact model name, e.g., 'RTX 4090'"),
    timeframe: str = Query("1d", description="1h, 1d, 1w, 1m"),
    db: AsyncSession = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Get OHLC (Open, High, Low, Close) chart data for a specific retail hardware model.
    """
    # Map timeframe to PostgreSQL date_trunc and interval
    trunc_map = {
        "1h": "hour",
        "1d": "day",
        "1w": "week",
        "1m": "month"
    }
    
    if timeframe not in trunc_map:
        raise HTTPException(status_code=400, detail="Invalid timeframe. Must be 1h, 1d, 1w, or 1m.")
    
    if db is None:
        return []
    
    trunc_level = trunc_map[timeframe]
    
    # Subquery: get min, max, first, last per time bucket
    # Note: In PostgreSQL, we can use distinct on or window functions.
    # We will use grouping with min/max, and array_agg or specialized logic for open/close,
    # but the easiest is subqueries or window functions.
    
    stmt = f"""
    WITH ranked AS (
        SELECT 
            date_trunc('{trunc_level}', timestamp) AS time_bucket,
            price,
            ROW_NUMBER() OVER(PARTITION BY date_trunc('{trunc_level}', timestamp) ORDER BY timestamp ASC) as rn_first,
            ROW_NUMBER() OVER(PARTITION BY date_trunc('{trunc_level}', timestamp) ORDER BY timestamp DESC) as rn_last
        FROM retail_price_history
        WHERE hardware_type = :hardware_type AND model_name = :model_name
    ),
    aggregated AS (
        SELECT 
            time_bucket,
            MIN(price) as low,
            MAX(price) as high
        FROM retail_price_history
        WHERE hardware_type = :hardware_type AND model_name = :model_name
        GROUP BY time_bucket
    )
    SELECT 
        a.time_bucket as time,
        (SELECT price FROM ranked WHERE time_bucket = a.time_bucket AND rn_first = 1 LIMIT 1) as open,
        a.high,
        a.low,
        (SELECT price FROM ranked WHERE time_bucket = a.time_bucket AND rn_last = 1 LIMIT 1) as close
    FROM aggregated a
    ORDER BY a.time_bucket ASC;
    """
    
    from sqlalchemy import text
    result = await db.execute(text(stmt), {"hardware_type": hardware_type, "model_name": model_name})
    rows = result.fetchall()
    
    chart_data = []
    for row in rows:
        chart_data.append({
            "time": row.time.isoformat() if row.time else None,
            "open": float(row.open) if row.open else 0,
            "high": float(row.high) if row.high else 0,
            "low": float(row.low) if row.low else 0,
            "close": float(row.close) if row.close else 0
        })
        
    return chart_data

@router.get("/enterprise")
async def get_enterprise_hardware(
    db: AsyncSession = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Get the latest prices for Enterprise B2B Hardware (H100, B200, DGX).
    """
    if db is None:
        return []

    stmt = """
    WITH RankedPrices AS (
        SELECT 
            model_name,
            platform,
            price,
            capacity_gb,
            product_url,
            is_official,
            timestamp,
            ROW_NUMBER() OVER(PARTITION BY model_name, platform ORDER BY timestamp DESC) as rn
        FROM retail_price_history
        WHERE hardware_type = 'enterprise_gpu'
    )
    SELECT * FROM RankedPrices WHERE rn = 1;
    """
    
    from sqlalchemy import text
    result = await db.execute(text(stmt))
    rows = result.fetchall()
    
    hardware = []
    for row in rows:
        hardware.append({
            "model_name": row.model_name,
            "platform": row.platform,
            "price": float(row.price),
            "capacity_gb": float(row.capacity_gb) if row.capacity_gb else None,
            "url": row.product_url,
            "is_official": row.is_official,
            "updated_at": row.timestamp.isoformat() if row.timestamp else None
        })
        
    return hardware
