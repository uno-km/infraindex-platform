from sqlalchemy import String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from shared.models.base import Base, UUIDMixin, TimeStampMixin
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shared.models.gpu_offering import PricingPlan

class PriceObservation(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "price_observations"
    
    pricing_plan_id: Mapped[str] = mapped_column(ForeignKey("pricing_plans.id"), index=True)
    
    source_price: Mapped[float] = mapped_column(Numeric(16, 6))
    source_currency: Mapped[str] = mapped_column(String(3), default="USD")
    source_unit: Mapped[str] = mapped_column(String(50)) # e.g. "hour", "second", "month"
    
    normalized_hourly_price: Mapped[float] = mapped_column(Numeric(16, 6))
    normalized_gpu_hour_price: Mapped[float] = mapped_column(Numeric(16, 6))
    normalized_vram_gb_hour_price: Mapped[float] = mapped_column(Numeric(16, 6))
    normalized_monthly_price: Mapped[float] = mapped_column(Numeric(16, 6))
    
    availability_status: Mapped[str] = mapped_column(String(50)) # available, unavailable, unknown
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    source_url: Mapped[str | None] = mapped_column(String(1024))
    
    pricing_plan: Mapped["PricingPlan"] = relationship("PricingPlan", back_populates="observations")
