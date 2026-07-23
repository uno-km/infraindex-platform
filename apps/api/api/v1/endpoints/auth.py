from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import hashlib

from apps.api.core.database import get_db
from apps.api.core.security import verify_password, create_access_token, get_password_hash
from apps.api.models.user import UserBas
from apps.api.models.login_history import LoginHistory

router = APIRouter()

@router.post("/login/admin")
async def login_admin_access_token(
    request: Request,
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, required for Admin Users.
    Only allows login if user is_admin=True.
    """
    result = await db.execute(select(UserBas).where(UserBas.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="The user doesn't have admin privileges")
        
    # Record Login History
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    history = LoginHistory(
        user_id=user.id,
        login_method="admin",
        ip_address=ip[:50] if ip else None,
        user_agent=ua
    )
    db.add(history)
    await db.commit()
        
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

# Mock endpoints for Social Login
@router.post("/login/social/{provider}")
async def login_social_mock(
    request: Request,
    provider: str,
    oauth_id: str,
    email: str,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Mock endpoint to simulate social login (Google/Naver/Kakao).
    In production, this would accept an OAuth code and verify via external provider.
    """
    if provider not in ["google", "naver", "kakao"]:
        raise HTTPException(status_code=400, detail="Unsupported provider")
        
    result = await db.execute(select(UserBas).where(UserBas.oauth_provider == provider, UserBas.oauth_id == oauth_id))
    user = result.scalar_one_or_none()
    
    if not user:
        # Auto register normal user
        nickname = f"user_{hashlib.md5(oauth_id.encode()).hexdigest()[:8]}"
        user = UserBas(
            email=email,
            nickname=nickname,
            oauth_provider=provider,
            oauth_id=oauth_id,
            is_admin=False
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    # Record Login History
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    history = LoginHistory(
        user_id=user.id,
        login_method=provider,
        ip_address=ip[:50] if ip else None,
        user_agent=ua
    )
    db.add(history)
    await db.commit()
        
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
