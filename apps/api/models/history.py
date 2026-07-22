from sqlalchemy import String, Float, DateTime, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from apps.api.models.base import Base, UUIDMixin

class PriceHistory(Base, UUIDMixin):
    """
    Time-Series Database Schema for historical GPU pricing.
    Unlike observations which might be overwritten, this table appends new rows
    to track price fluctuations over time (for analytical charting).
    """
    __tablename__ = "price_history"
    
    provider_id: Mapped[str] = mapped_column(String(50), index=True)
    gpu_model: Mapped[str] = mapped_column(String(100), index=True)
    vram_gb: Mapped[float] = mapped_column(Float)
    price_per_hour: Mapped[float] = mapped_column(Float)
    availability_status: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (
        Index('ix_price_history_provider_gpu_time', 'provider_id', 'gpu_model', 'timestamp'),
    )
