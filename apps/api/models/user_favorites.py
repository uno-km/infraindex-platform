from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.api.models.base import Base, UUIDMixin, TimeStampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.api.models.user import UserBas

class UserFavorite(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "user_fvrt"

    user_id: Mapped[str] = mapped_column(ForeignKey("user_bas.id", ondelete="CASCADE"), index=True)
    
    target_type: Mapped[str] = mapped_column(String(50), index=True) # e.g. "gpu", "cpu", "news"
    target_id: Mapped[str] = mapped_column(String(255), index=True)
    
    user: Mapped["UserBas"] = relationship("UserBas", back_populates="favorites")
