from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from typing import List, Dict, Any
from datetime import datetime, timedelta, timezone

from apps.api.core.database import get_db
from apps.services.financial.models import FinancialMarketHistory
from apps.services.gpu.models_history import PriceHistory
from apps.services.retail.models import RetailPriceHistory

router = APIRouter()

@router.get("/correlation", response_model=List[Dict[str, Any]])
async def get_insight_correlation(
    timeframe: str = Query("1w", description="Timeframe (e.g., 1d, 1w, 1mo, 3mo)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns percentage change (% diff) from the start of the timeframe 
    for cloud GPU, retail GPU, and semiconductor stocks, normalized to base 0%.
    """
    if db is None:
        return []

    # Calculate cutoff time
    now = datetime.now(timezone.utc)
    if timeframe == "1d":
        cutoff = now - timedelta(days=1)
    elif timeframe == "1w":
        cutoff = now - timedelta(days=7)
    elif timeframe == "1mo":
        cutoff = now - timedelta(days=30)
    elif timeframe == "3mo":
        cutoff = now - timedelta(days=90)
    else:
        raise HTTPException(status_code=400, detail="Unsupported timeframe. Use 1d, 1w, 1mo, 3mo.")

    # 1. Fetch baseline (oldest price in timeframe) and latest price for Stocks
    stmt_financial = select(
        FinancialMarketHistory.symbol, 
        FinancialMarketHistory.close, 
        FinancialMarketHistory.timestamp
    ).where(FinancialMarketHistory.timestamp >= cutoff).order_by(FinancialMarketHistory.timestamp.asc())
    
    financial_results = await db.execute(stmt_financial)
    financial_records = financial_results.all()
    
    financial_baselines = {}
    financial_latest = {}
    
    for symbol, close, ts in financial_records:
        if symbol not in financial_baselines:
            financial_baselines[symbol] = close
        financial_latest[symbol] = close

    # 2. Fetch baseline and latest for Retail GPUs (Average price)
    stmt_retail = select(
        RetailPriceHistory.model_name,
        RetailPriceHistory.price,
        RetailPriceHistory.timestamp
    ).where(RetailPriceHistory.timestamp >= cutoff).order_by(RetailPriceHistory.timestamp.asc())
    
    retail_results = await db.execute(stmt_retail)
    retail_records = retail_results.all()
    
    retail_baselines = {}
    retail_latest = {}
    
    for model, price, ts in retail_records:
        if model not in retail_baselines:
            retail_baselines[model] = price
        retail_latest[model] = price

    # 3. Combine results into percentage change
    correlations = []
    
    # Financials
    for symbol, base_price in financial_baselines.items():
        latest = financial_latest[symbol]
        pct_change = ((latest - base_price) / base_price) * 100 if base_price else 0
        correlations.append({
            "asset": symbol,
            "category": "Market",
            "base_price": base_price,
            "latest_price": latest,
            "percentage_change": round(pct_change, 2)
        })
        
    # Retail
    for model, base_price in retail_baselines.items():
        latest = retail_latest[model]
        pct_change = ((latest - base_price) / base_price) * 100 if base_price else 0
        correlations.append({
            "asset": f"Retail {model}",
            "category": "Retail Hardware",
            "base_price": base_price,
            "latest_price": latest,
            "percentage_change": round(pct_change, 2)
        })
        
    return correlations
