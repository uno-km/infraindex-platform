from fastapi import APIRouter, Depends, Response
from fastapi_cache.decorator import cache
from apps.server.core.cache_utils import get_cache_control
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any
from collections import defaultdict
from shared.db.session import get_db
from shared.models.ai_pricing import AIModelMaster, AIModelPriceHistory

router = APIRouter()

@router.get("/latest", response_model=Dict[str, List[Dict[str, Any]]], dependencies=[Depends(get_cache_control(max_age=60, s_maxage=3600))])
@cache(expire=3600)  # Redis Shared Cache
async def get_latest_ai_pricing(db: AsyncSession = Depends(get_db)):
    """
    체급별(Tier) AI 모델 최신 가격 정보를 반환합니다.
    """
    stmt = (
        select(AIModelMaster, AIModelPriceHistory)
        .join(AIModelPriceHistory, AIModelMaster.id == AIModelPriceHistory.model_id)
        .order_by(AIModelPriceHistory.collected_date.desc())
    )
    result = await db.execute(stmt)
    rows = result.all()
    
    # 중복 모델 제거 (가장 최신 날짜만 유지)
    latest_prices = {}
    for master, history in rows:
        if master.model_code not in latest_prices:
            latest_prices[master.model_code] = {
                "id": str(master.id),
                "model_code": master.model_code,
                "name": master.name,
                "provider": master.provider,
                "tier": master.tier,
                "context_length": master.context_length,
                "input_price_1m": history.input_price_1m,
                "output_price_1m": history.output_price_1m,
                "collected_date": history.collected_date.isoformat()
            }
            
    # 그룹화 by Tier
    grouped_by_tier = defaultdict(list)
    for model_info in latest_prices.values():
        grouped_by_tier[model_info["tier"]].append(model_info)
        
    return grouped_by_tier


@router.get("/history", response_model=Dict[str, Any], dependencies=[Depends(get_cache_control(max_age=60, s_maxage=3600))])
@cache(expire=3600)
async def get_ai_pricing_history(db: AsyncSession = Depends(get_db)):
    """
    선형 차트(Line Chart)를 그리기 위한 시계열 가격 이력을 반환합니다.
    """
    stmt = (
        select(AIModelMaster, AIModelPriceHistory)
        .join(AIModelPriceHistory, AIModelMaster.id == AIModelPriceHistory.model_id)
        .order_by(AIModelPriceHistory.collected_date.asc())
    )
    result = await db.execute(stmt)
    rows = result.all()
    
    history_data = defaultdict(lambda: {"name": "", "provider": "", "data": []})
    
    for master, history in rows:
        history_data[master.model_code]["name"] = master.name
        history_data[master.model_code]["provider"] = master.provider
        history_data[master.model_code]["tier"] = master.tier
        history_data[master.model_code]["data"].append({
            "date": history.collected_date.isoformat(),
            "input_price": history.input_price_1m,
            "output_price": history.output_price_1m
        })
        
    return history_data
