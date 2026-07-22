from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from apps.api.models.base import Base, UUIDMixin, TimeStampMixin
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from apps.api.models.offering import OfferingGpuConfiguration

class GpuManufacturer(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "gpu_manufacturers"
    
    name: Mapped[str] = mapped_column(String(255), unique=True)
    
    models: Mapped[List["GpuModel"]] = relationship("GpuModel", back_populates="manufacturer")

class GpuModel(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "gpu_models"
    
    manufacturer_id: Mapped[str] = mapped_column(ForeignKey("gpu_manufacturers.id"), index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True) # e.g. "H100"
    
    manufacturer: Mapped["GpuManufacturer"] = relationship("GpuManufacturer", back_populates="models")
    variants: Mapped[List["GpuVariant"]] = relationship("GpuVariant", back_populates="model")

class GpuVariant(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "gpu_variants"
    
    model_id: Mapped[str] = mapped_column(ForeignKey("gpu_models.id"), index=True)
    name: Mapped[str] = mapped_column(String(255)) # e.g. "PCIe 80GB"
    form_factor: Mapped[str | None] = mapped_column(String(50)) # PCIe, SXM, NVL
    vram_gb: Mapped[float] = mapped_column(Float)
    
    model: Mapped["GpuModel"] = relationship("GpuModel", back_populates="variants")
    configurations: Mapped[List["OfferingGpuConfiguration"]] = relationship("OfferingGpuConfiguration", back_populates="variant")
