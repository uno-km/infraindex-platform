from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from apps.api.models.base import Base, UUIDMixin, TimeStampMixin
from typing import List

class StorageProvider(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "storage_providers"
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

class StorageTier(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "storage_tiers"
    provider_id: Mapped[str] = mapped_column(ForeignKey("storage_providers.id"), index=True)
    name: Mapped[str] = mapped_column(String(255)) # e.g. "S3 Standard", "S3 Glacier"
    price_per_gb_month: Mapped[float] = mapped_column(Float)
    egress_price_per_gb: Mapped[float] = mapped_column(Float)
    
    provider: Mapped["StorageProvider"] = relationship()

class StoragePriceHistory(Base, UUIDMixin):
    """
    시계열 스토리지 가격 이력 테이블.
    - tbl_storage_prc_hist
    """
    __tablename__ = "tbl_storage_prc_hist"

    prv_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    storage_mdl: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    prc_pgb_mth: Mapped[float] = mapped_column(Float, nullable=False)
    ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )
