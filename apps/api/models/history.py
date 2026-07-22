from sqlalchemy import String, Numeric, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from apps.api.models.base import Base, UUIDMixin


class PriceHistory(Base, UUIDMixin):
    """
    시계열 GPU 가격 이력 테이블.
    - 매 수집마다 row 추가 (UPDATE 없음, 순수 append-only)
    - price_per_hour: Numeric(12,6) — 부동소수점 오차 방지
    - vram_gb: Numeric(8,2) — 소수점 2자리 충분
    - 인덱스: (provider_id, gpu_model, timestamp DESC) — 차트/이력 쿼리 최적화
    """
    __tablename__ = "price_history"

    provider_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    hardware_type: Mapped[str] = mapped_column(String(20), nullable=False, default="gpu")
    
    # GPU Fields
    gpu_model: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    vram_gb: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True, default=0)
    
    # CPU Fields
    cpu_model: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    cores: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    
    price_per_hour: Mapped[float] = mapped_column(Numeric(12, 6), nullable=False)
    availability_status: Mapped[str] = mapped_column(String(50), nullable=False, default="unknown")
    provider_link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    sys_ram_gb: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    tdp_w: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )

    __table_args__ = (
        # 차트/이력 쿼리: WHERE provider_id=X AND gpu_model ILIKE Y ORDER BY timestamp DESC
        Index(
            "ix_price_history_provider_gpu_time",
            "provider_id", "gpu_model", "timestamp",
        ),
        # 일별 집계 쿼리: WHERE gpu_model ILIKE X AND timestamp >= Y
        Index(
            "ix_price_history_gpu_time",
            "gpu_model", "timestamp",
        ),
    )

