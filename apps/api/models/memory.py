from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from apps.api.models.base import Base, UUIDMixin, TimeStampMixin
from typing import List

class MemoryManufacturer(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "memory_manufacturers"
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

class MemoryModule(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "memory_modules"
    manufacturer_id: Mapped[str] = mapped_column(ForeignKey("memory_manufacturers.id"), index=True)
    type: Mapped[str] = mapped_column(String(50)) # DRAM, HBM, NAND
    capacity_gb: Mapped[float] = mapped_column(Float)
    speed_mhz: Mapped[int | None] = mapped_column(Integer)
    
    manufacturer: Mapped["MemoryManufacturer"] = relationship()
