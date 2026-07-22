from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from apps.api.models.base import Base, UUIDMixin

class User(Base, UUIDMixin):
    """
    사용자 모델 (일반 유저 및 어드민 통합)
    일반 유저는 OAuth(google, naver, kakao) Provider ID를 통해 식별
    어드민 유저는 email을 통해 식별되며 is_admin=True 속성 가짐
    """
    __tablename__ = "users"

    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # OAuth
    oauth_provider: Mapped[str | None] = mapped_column(String(50), nullable=True) # google, naver, kakao
    oauth_id: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
