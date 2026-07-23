from sqlalchemy import String, Numeric, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from apps.api.models.base import Base, UUIDMixin


class GpuPriceHistory(Base, UUIDMixin):
    """
    시계열 GPU 가격 이력 테이블.
    - tbl_gpu_prc_hist
    """
    __tablename__ = "tbl_gpu_prc_hist"

    prv_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    hw_typ: Mapped[str] = mapped_column(String(20), nullable=False, default="gpu")
    
    # GPU Fields
    gpu_mdl: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    vram_gb: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True, default=0)
    
    # CPU Fields
    cpu_mdl: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    core_cnt: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    
    prc_ph: Mapped[float] = mapped_column(Numeric(12, 6), nullable=False)
    avl_st: Mapped[str] = mapped_column(String(50), nullable=False, default="unknown")
    prv_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    sys_ram: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    tdp_w: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )

    __table_args__ = (
        Index(
            "idx_gpu_prc_prv_ts",
            "prv_id", "ts",
        ),
        Index(
            "idx_gpu_prc_mdl_ts",
            "gpu_mdl", "ts",
        ),
    )


