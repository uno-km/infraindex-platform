from sqlalchemy import String, Numeric, DateTime, Index, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from apps.api.models.base import Base, UUIDMixin


class RetailPriceHistory(Base, UUIDMixin):
    """
    소매(Retail) 가격 이력 테이블.
    - 실제 e-commerce (쿠팡, 다나와, 아마존 등) 및 공식 홈페이지의 구매 가격
    - 매 수집마다 row 추가 (append-only)
    - price: Numeric(15,2) — 원화(KRW)와 달러(USD) 등 범용적으로 저장
    """
    __tablename__ = "retail_price_history"

    platform: Mapped[str] = mapped_column(String(50), index=True, nullable=False) # e.g., danawa, coupang, amazon
    hardware_type: Mapped[str] = mapped_column(String(20), nullable=False) # gpu, cpu, ram
    
    manufacturer: Mapped[str | None] = mapped_column(String(50), nullable=True) # nvidia, amd, intel, samsung, skhynix
    model_name: Mapped[str] = mapped_column(String(200), index=True, nullable=False) # e.g., RTX 4090, Ryzen 9 7950X, DDR5 32GB PC5-44800
    capacity_gb: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True) # 24 (VRAM or RAM capacity)
    
    price: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="KRW") # KRW, USD
    
    product_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_official: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False) # True if MSRP or official foundry price
    
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )

    __table_args__ = (
        # OHLC 쿼리 성능을 위한 인덱스: WHERE model_name=X AND hardware_type=Y ORDER BY timestamp
        Index(
            "ix_retail_price_hardware_model_time",
            "hardware_type", "model_name", "timestamp",
        ),
        # 플랫폼별 최근 가격 조회용 인덱스
        Index(
            "ix_retail_price_platform_model_time",
            "platform", "model_name", "timestamp",
        ),
    )
