from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
