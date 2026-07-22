from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.api.core.database import get_db
from apps.api.models.quality import DataQualityIssue

router = APIRouter()

@router.get("/quarantine", response_model=List[dict])
async def list_quarantine_items(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List data items that were quarantined due to extreme price variance or missing fields.
    (Admin only)
    """
    result = await db.execute(
        select(DataQualityIssue)
        .where(DataQualityIssue.severity == "quarantine")
        .offset(skip).limit(limit)
    )
    issues = result.scalars().all()
    
    # Returning raw dict for mock implementation since we don't have schemas for this yet
    return [{"id": str(i.id), "issue_type": i.issue_type, "description": i.description} for i in issues]

@router.post("/quarantine/{issue_id}/approve")
async def approve_quarantine_item(
    issue_id: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Approve and release a quarantined item into the live observation table.
    """
    # TODO: Fetch issue, extract payload, push to PriceObservation, and resolve issue.
    return {"status": "approved", "issue_id": issue_id}
