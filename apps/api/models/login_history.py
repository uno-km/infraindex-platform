from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid
from typing import TYPE_CHECKING

from apps.api.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from apps.api.models.user import UserBas

class LoginHistory(Base, UUIDMixin):
    __tablename__ = "login_history"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user_bas.id", ondelete="CASCADE"), nullable=False)
    login_method: Mapped[str] = mapped_column(String(50), nullable=False, comment="admin, google, naver, kakao")
    ip_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["UserBas"] = relationship("UserBas", back_populates="login_histories")
