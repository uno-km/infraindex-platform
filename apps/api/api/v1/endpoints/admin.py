from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.api.core.database import get_db
from apps.api.core.config import settings
from apps.api.models.quality import DataQualityIssue

router = APIRouter()


# FIX-01: 관리자 인증 의존성
async def verify_admin(x_api_key: str = Header(..., alias="X-Admin-API-Key")) -> None:
    """
    Admin API Key 인증.
    환경변수 ADMIN_API_KEY 설정 필수. 미설정 시 503 반환.
    요청 헤더: X-Admin-API-Key: <key>
    """
    if not settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin API Key is not configured on this server. Set ADMIN_API_KEY environment variable.",
        )
    if x_api_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Admin API Key.",
        )


@router.get("/quarantine", response_model=List[dict], dependencies=[Depends(verify_admin)])
async def list_quarantine_items(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List data items that were quarantined due to extreme price variance or missing fields.
    (Admin only — requires X-Admin-API-Key header)
    """
    result = await db.execute(
        select(DataQualityIssue)
        .where(DataQualityIssue.severity == "quarantine")
        .offset(skip).limit(limit)
    )
    issues = result.scalars().all()
    return [
        {
            "id": str(i.id),
            "issue_type": i.issue_type,
            "severity": i.severity,
            "description": i.description,
            "observation_id": str(i.observation_id) if i.observation_id else None,
            "run_id": str(i.run_id),
            "created_at": i.created_at.isoformat(),
        }
        for i in issues
    ]


@router.post(
    "/quarantine/{issue_id}/approve",
    dependencies=[Depends(verify_admin)],
)
async def approve_quarantine_item(
    issue_id: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Approve and release a quarantined item.
    (Admin only — requires X-Admin-API-Key header)
    """
    result = await db.execute(
        select(DataQualityIssue).where(DataQualityIssue.id == issue_id)
    )
    issue = result.scalar_one_or_none()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # 심각도를 'resolved'로 변경하여 quarantine 해제
    issue.severity = "resolved"
    await db.commit()
    return {"status": "approved", "issue_id": issue_id}


@router.post(
    "/quarantine/{issue_id}/reject",
    dependencies=[Depends(verify_admin)],
)
async def reject_quarantine_item(
    issue_id: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Reject (permanently dismiss) a quarantined item.
    (Admin only — requires X-Admin-API-Key header)
    """
    result = await db.execute(
        select(DataQualityIssue).where(DataQualityIssue.id == issue_id)
    )
    issue = result.scalar_one_or_none()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    issue.severity = "rejected"
    await db.commit()
    return {"status": "rejected", "issue_id": issue_id}
