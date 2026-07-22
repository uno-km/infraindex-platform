from sqlalchemy import String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from apps.api.models.base import Base, UUIDMixin, TimeStampMixin
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from apps.api.models.provider import Provider, ProviderRegion
    from apps.api.models.hardware import GpuVariant

class InstanceOffering(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "instance_offerings"
    
    provider_id: Mapped[str] = mapped_column(ForeignKey("providers.id"), index=True)
    region_id: Mapped[str | None] = mapped_column(ForeignKey("provider_regions.id"), index=True)
    machine_type_name: Mapped[str] = mapped_column(String(255), index=True) # e.g. "g5.2xlarge" or "1x A100"
    
    includes_cpu: Mapped[bool] = mapped_column(Boolean, default=True)
    includes_ram: Mapped[bool] = mapped_column(Boolean, default=True)
    includes_local_storage: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    provider: Mapped["Provider"] = relationship("Provider", back_populates="offerings")
    region: Mapped["ProviderRegion | None"] = relationship("ProviderRegion", back_populates="offerings")
    gpu_configuration: Mapped[List["OfferingGpuConfiguration"]] = relationship("OfferingGpuConfiguration", back_populates="offering")
    pricing_plans: Mapped[List["PricingPlan"]] = relationship("PricingPlan", back_populates="offering")

class OfferingGpuConfiguration(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "offering_gpu_configurations"
    
    offering_id: Mapped[str] = mapped_column(ForeignKey("instance_offerings.id"), index=True)
    gpu_variant_id: Mapped[str] = mapped_column(ForeignKey("gpu_variants.id"), index=True)
    count: Mapped[int] = mapped_column(Integer)
    
    offering: Mapped["InstanceOffering"] = relationship("InstanceOffering", back_populates="gpu_configuration")
    variant: Mapped["GpuVariant"] = relationship("GpuVariant", back_populates="configurations")

class PricingPlan(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "pricing_plans"
    
    offering_id: Mapped[str] = mapped_column(ForeignKey("instance_offerings.id"), index=True)
    plan_type: Mapped[str] = mapped_column(String(50)) # on_demand, spot, reserved, serverless
    billing_increment_seconds: Mapped[int] = mapped_column(Integer, default=3600)
    minimum_billing_seconds: Mapped[int] = mapped_column(Integer, default=3600)
    
    offering: Mapped["InstanceOffering"] = relationship("InstanceOffering", back_populates="pricing_plans")
    observations: Mapped[List["PriceObservation"]] = relationship("PriceObservation", back_populates="pricing_plan")
