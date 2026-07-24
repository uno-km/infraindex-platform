from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError

from apps.api.core.database import get_db
from apps.api.core.config import settings
from apps.api.models.quality import DataQualityIssue
from apps.api.models.user import UserBas as User
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


# --- 3. Manual Batch Trigger ---

class BatchTriggerRequest(BaseModel):
    target: str = "all"  # "all", "gpu", "retail", "financial", "news", or specific provider e.g. "aws"

@router.post("/batch/trigger")
async def trigger_manual_batch(
    background_tasks: BackgroundTasks,
    request_data: BatchTriggerRequest = BatchTriggerRequest(),
) -> Any:
    """
    Manually trigger batch crawler job in the background.
    Target options: 'all', 'gpu', 'retail', 'financial', 'news', or a specific provider (e.g. 'aws').
    """
    from apps.worker.batch_runner import run_batch

    background_tasks.add_task(run_batch, request_data.target)
    return {
        "status": "scheduled",
        "message": f"Batch job triggered for target '{request_data.target}' in background.",
        "target": request_data.target,
    }


# --- 4. Schedule Refresh ---

@router.post("/schedules/refresh", dependencies=[Depends(verify_admin)])
async def trigger_schedule_refresh() -> Any:
    """
    Refresh the batch schedules loaded in memory (Singleton).
    This triggers the Celery worker to reload schedules from the database.
    """
    from apps.worker.tasks.orchestrator import refresh_schedules as refresh_schedules_task
    
    # Send a celery task to the worker to reload its schedule singleton
    refresh_schedules_task.delay()
    
    return {
        "status": "triggered",
        "message": "Celery schedule refresh triggered successfully.",
    }


# --- 5. User Management ---

@router.get("/users", dependencies=[Depends(verify_admin)])
async def list_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List all users.
    """
    from apps.api.models.user import UserBas
    result = await db.execute(
        select(UserBas).order_by(UserBas.created_at.desc()).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    return [
        {
            "id": str(u.id),
            "email": u.email,
            "nickname": u.nickname,
            "oauth_provider": u.oauth_provider,
            "is_admin": u.is_admin,
            "is_active": u.is_active,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in users
    ]

@router.get("/login-history", dependencies=[Depends(verify_admin)])
async def list_login_history(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List login history for all users.
    """
    from apps.api.models.login_history import LoginHistory
    from sqlalchemy.orm import joinedload
    
    result = await db.execute(
        select(LoginHistory)
        .options(joinedload(LoginHistory.user))
        .order_by(LoginHistory.created_at.desc())
        .offset(skip).limit(limit)
    )
    histories = result.scalars().all()
    return [
        {
            "id": str(h.id),
            "user_id": str(h.user_id),
            "nickname": h.user.nickname if h.user else "Unknown",
            "login_method": h.login_method,
            "ip_address": h.ip_address,
            "user_agent": h.user_agent,
            "created_at": h.created_at.isoformat() if h.created_at else None,
        }
        for h in histories
    ]

# --- 6. Batch History ---

@router.get("/batch/history", dependencies=[Depends(verify_admin)])
async def list_batch_history(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List batch execution history.
    """
    from apps.api.models.batch_schedule import SysBatSchHist
    result = await db.execute(
        select(SysBatSchHist).order_by(SysBatSchHist.seq.desc()).offset(skip).limit(limit)
    )
    histories = result.scalars().all()
    return [
        {
            "seq": h.seq,
            "bat_id": h.bat_id,
            "job_id": h.job_id,
            "status": h.status,
            "start_dt": h.start_dt.isoformat() if h.start_dt else None,
            "end_dt": h.end_dt.isoformat() if h.end_dt else None,
            "err_msg": h.err_msg,
            "crt_dt": h.crt_dt.isoformat() if h.crt_dt else None,
        }
        for h in histories
    ]
