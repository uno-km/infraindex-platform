import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from apps.api.api.deps import get_db
from apps.api.core.security import verify_token
from apps.api.models.user import UserBas
from apps.api.models.user_favorites import UserFavorite

router = APIRouter()

async def get_current_user(
    token_payload: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
) -> UserBas:
    user_id_str = token_payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format",
        )
        
    result = await db.execute(
        select(UserBas)
        .options(selectinload(UserBas.settings))
        .where(UserBas.id == user_id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/me")
async def read_user_me(current_user: UserBas = Depends(get_current_user)) -> Any:
    """
    현재 로그인된 유저 정보 반환
    """
    settings = None
    if current_user.settings:
        settings = {
            "theme": current_user.settings.theme,
            "email_notifications": current_user.settings.email_notifications,
            "language": current_user.settings.language,
        }
        
    return {
        "id": current_user.id,
        "email": current_user.email,
        "nickname": current_user.nickname,
        "is_admin": current_user.is_admin,
        "oauth_provider": current_user.oauth_provider,
        "settings": settings
    }

class FavoriteRequest(BaseModel):
    target_type: str
    target_id: str

@router.get("/favorites")
async def get_favorites(
    current_user: UserBas = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    유저의 관심(Favorites) 항목 리스트 조회
    """
    result = await db.execute(
        select(UserFavorite).where(UserFavorite.user_id == current_user.id)
    )
    favorites = result.scalars().all()
    return [{"id": f.id, "target_type": f.target_type, "target_id": f.target_id, "created_at": f.created_at} for f in favorites]

@router.post("/favorites")
async def add_favorite(
    req: FavoriteRequest,
    current_user: UserBas = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    유저 관심 항목 추가
    """
    # Check if already exists
    result = await db.execute(
        select(UserFavorite).where(
            UserFavorite.user_id == current_user.id,
            UserFavorite.target_type == req.target_type,
            UserFavorite.target_id == req.target_id
        )
    )
    if result.scalars().first():
        return {"status": "already_exists"}
        
    fav = UserFavorite(
        user_id=current_user.id,
        target_type=req.target_type,
        target_id=req.target_id
    )
    db.add(fav)
    await db.commit()
    await db.refresh(fav)
    
    return {"status": "success", "id": fav.id}

@router.delete("/favorites/{target_type}/{target_id}")
async def remove_favorite(
    target_type: str,
    target_id: str,
    current_user: UserBas = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    유저 관심 항목 삭제
    """
    result = await db.execute(
        select(UserFavorite).where(
            UserFavorite.user_id == current_user.id,
            UserFavorite.target_type == target_type,
            UserFavorite.target_id == target_id
        )
    )
    fav = result.scalars().first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
        
    await db.delete(fav)
    await db.commit()
    
    return {"status": "success"}
