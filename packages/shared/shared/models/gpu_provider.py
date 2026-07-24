from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from shared.models.base import Base, UUIDMixin, TimeStampMixin
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from shared.models.gpu_offering import InstanceOffering

class Provider(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "providers"
    
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    official_homepage: Mapped[str | None] = mapped_column(String(1024))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str | None] = mapped_column(Text)
    
    regions: Mapped[List["ProviderRegion"]] = relationship("ProviderRegion", back_populates="provider")
    offerings: Mapped[List["InstanceOffering"]] = relationship("InstanceOffering", back_populates="provider")

class ProviderRegion(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "provider_regions"
    
    provider_id: Mapped[str] = mapped_column(ForeignKey("providers.id"), index=True)
    provider_region_id: Mapped[str] = mapped_column(String(255), index=True) # e.g. "us-east-1"
    name: Mapped[str] = mapped_column(String(255))
    country: Mapped[str | None] = mapped_column(String(2)) # ISO code
    
    provider: Mapped["Provider"] = relationship("Provider", back_populates="regions")
    offerings: Mapped[List["InstanceOffering"]] = relationship("InstanceOffering", back_populates="region")
