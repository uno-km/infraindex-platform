from sqlalchemy import String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from apps.api.models.base import Base, UUIDMixin, TimeStampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.services.gpu.models_hardware import GpuModel

class PriceAlert(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "price_alerts"
    
    user_email: Mapped[str] = mapped_column(String(255), index=True)
    gpu_model_id: Mapped[str | None] = mapped_column(ForeignKey("gpu_models.id"), index=True)
    target_price: Mapped[float] = mapped_column(Numeric(16, 6))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    gpu_model: Mapped["GpuModel | None"] = relationship("GpuModel")
