from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.api.models.base import Base, UUIDMixin, TimeStampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.api.models.user import UserBas

class UserSettings(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "user_stng"

    user_id: Mapped[str] = mapped_column(ForeignKey("user_bas.id", ondelete="CASCADE"), unique=True, index=True)
    
    theme: Mapped[str] = mapped_column(String(20), default="dark")
    email_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    language: Mapped[str] = mapped_column(String(10), default="ko")
    
    user: Mapped["UserBas"] = relationship("UserBas", back_populates="settings")
