from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from apps.api.core.database import get_db
from apps.api.models.alerts import AlertRule, AlertHistory

router = APIRouter()

class AlertRuleCreate(BaseModel):
    target: str
    alert_type: str
    price_threshold: Optional[float] = None
    is_active: bool = True

class AlertRuleResponse(BaseModel):
    id: UUID
    target: str
    alert_type: str
    price_threshold: Optional[float]
    is_active: bool

    class Config:
        from_attributes = True

class AlertHistoryResponse(BaseModel):
    id: UUID
    rule_id: UUID
    title: str
    message: str
    link_url: Optional[str]
    is_read: bool

    class Config:
        from_attributes = True


@router.get("/rules", response_model=List[AlertRuleResponse])
async def get_alert_rules(db: AsyncSession = Depends(get_db)):
    stmt = select(AlertRule).order_by(AlertRule.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/rules", response_model=AlertRuleResponse)
async def create_alert_rule(rule_in: AlertRuleCreate, db: AsyncSession = Depends(get_db)):
    new_rule = AlertRule(**rule_in.model_dump())
    db.add(new_rule)
    await db.commit()
    await db.refresh(new_rule)
    return new_rule

@router.get("/history", response_model=List[AlertHistoryResponse])
async def get_alert_history(db: AsyncSession = Depends(get_db)):
    stmt = select(AlertHistory).order_by(AlertHistory.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/history/{history_id}/read", response_model=AlertHistoryResponse)
async def mark_alert_read(history_id: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(AlertHistory).where(AlertHistory.id == history_id)
    result = await db.execute(stmt)
    history = result.scalar_one_or_none()
    
    if not history:
        raise HTTPException(status_code=404, detail="Alert not found")
        
    history.is_read = True
    await db.commit()
    await db.refresh(history)
    return history
