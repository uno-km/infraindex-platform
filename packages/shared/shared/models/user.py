from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from typing import TYPE_CHECKING, List

from shared.models.base import Base, UUIDMixin, TimeStampMixin

if TYPE_CHECKING:
    from shared.models.login_history import LoginHistory
    from shared.models.user_favorites import UserFavorite
    from shared.models.user_settings import UserSettings
    from shared.models.user_follows import UserFollow

class UserBas(Base, UUIDMixin, TimeStampMixin):
    """
    사용자 모델 (일반 유저 및 어드민 통합)
    일반 유저는 OAuth(google, naver, kakao) Provider ID를 통해 식별
    어드민 유저는 email을 통해 식별되며 is_admin=True 속성 가짐
    """
    __tablename__ = "user_bas"

    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    nickname: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True)
    
    # OAuth
    oauth_provider: Mapped[str | None] = mapped_column(String(50), nullable=True) # google, naver, kakao
    oauth_id: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    login_histories: Mapped[List["LoginHistory"]] = relationship("LoginHistory", back_populates="user", cascade="all, delete-orphan")
    favorites: Mapped[List["UserFavorite"]] = relationship("UserFavorite", back_populates="user", cascade="all, delete-orphan")
    settings: Mapped["UserSettings"] = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    followers: Mapped[List["UserFollow"]] = relationship(
        "UserFollow", 
        foreign_keys="[UserFollow.following_id]", 
        back_populates="following",
        cascade="all, delete-orphan"
    )
    following: Mapped[List["UserFollow"]] = relationship(
        "UserFollow", 
        foreign_keys="[UserFollow.follower_id]", 
        back_populates="follower",
        cascade="all, delete-orphan"
    )
