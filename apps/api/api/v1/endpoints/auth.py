from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.api.core.database import get_db
from apps.api.core.security import verify_password, create_access_token, get_password_hash
from apps.api.models.user import User

router = APIRouter()

@router.post("/login/admin")
async def login_admin_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, required for Admin Users.
    Only allows login if user is_admin=True.
    """
    if form_data.username == "admin" and form_data.password == "1234":
        # Bypass DB for hardcoded admin as requested
        access_token = create_access_token(subject="admin_user_id")
        return {"access_token": access_token, "token_type": "bearer"}

    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="The user doesn't have admin privileges")
        
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

# Mock endpoints for Social Login
@router.post("/login/social/{provider}")
async def login_social_mock(
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
        
    result = await db.execute(select(User).where(User.oauth_provider == provider, User.oauth_id == oauth_id))
    user = result.scalar_one_or_none()
    
    if not user:
        # Auto register normal user
        user = User(
            email=email,
            oauth_provider=provider,
            oauth_id=oauth_id,
            is_admin=False
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
