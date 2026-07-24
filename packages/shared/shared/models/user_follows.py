from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from shared.models.base import Base, TimeStampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shared.models.user import UserBas

class UserFollow(Base, TimeStampMixin):
    __tablename__ = "user_flw"
    
    # Using composite primary key for follows
    follower_id: Mapped[str] = mapped_column(ForeignKey("user_bas.id", ondelete="CASCADE"), primary_key=True)
    following_id: Mapped[str] = mapped_column(ForeignKey("user_bas.id", ondelete="CASCADE"), primary_key=True)
    
    follower: Mapped["UserBas"] = relationship("UserBas", foreign_keys=[follower_id], back_populates="following")
    following: Mapped["UserBas"] = relationship("UserBas", foreign_keys=[following_id], back_populates="followers")
