from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError

from apps.api.core.database import get_db
from apps.api.core.config import settings
from apps.api.models.quality import DataQualityIssue
from apps.api.models.user import User
from apps.api.models.system_config import CrawlerConfig
from pydantic import BaseModel

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/admin")

async def verify_admin(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Verify JWT Token and ensure user is an admin.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None or not user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return user


# --- 1. System Config (Crawler DB Migration) ---

class CrawlerConfigUpdate(BaseModel):
    interval_minutes: int
    is_active: bool
    target_urls: str | None = None

@router.get("/config/crawlers", dependencies=[Depends(verify_admin)])
async def list_crawlers(db: AsyncSession = Depends(get_db)) -> Any:
    result = await db.execute(select(CrawlerConfig))
    return result.scalars().all()

@router.put("/config/crawlers/{name}", dependencies=[Depends(verify_admin)])
async def update_crawler_config(
    name: str,
    config_in: CrawlerConfigUpdate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    result = await db.execute(select(CrawlerConfig).where(CrawlerConfig.name == name))
    config = result.scalar_one_or_none()
    if not config:
        # Create it if it doesn't exist
        config = CrawlerConfig(name=name, **config_in.dict())
        db.add(config)
    else:
        config.interval_minutes = config_in.interval_minutes
        config.is_active = config_in.is_active
        config.target_urls = config_in.target_urls
    await db.commit()
    await db.refresh(config)
    return config

# --- 2. Data Quality (Quarantine) ---

@router.get("/quarantine", response_model=List[dict], dependencies=[Depends(verify_admin)])
async def list_quarantine_items(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
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
    result = await db.execute(select(DataQualityIssue).where(DataQualityIssue.id == issue_id))
    issue = result.scalar_one_or_none()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
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
    result = await db.execute(select(DataQualityIssue).where(DataQualityIssue.id == issue_id))
    issue = result.scalar_one_or_none()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    issue.severity = "rejected"
    await db.commit()
    return {"status": "rejected", "issue_id": issue_id}
