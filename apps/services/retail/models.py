from sqlalchemy import String, Numeric, DateTime, Index, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from apps.api.models.base import Base, UUIDMixin


class RtlPriceHistory(Base, UUIDMixin):
    """
    소매(Retail) 가격 이력 테이블.
    - tbl_rtl_prc_hist
    """
    __tablename__ = "tbl_rtl_prc_hist"

    pltf_nm: Mapped[str] = mapped_column(String(50), index=True, nullable=False) # e.g., danawa, coupang, amazon
    hw_typ: Mapped[str] = mapped_column(String(20), nullable=False) # gpu, cpu, ram
    
    mfg_nm: Mapped[str | None] = mapped_column(String(50), nullable=True) # nvidia, amd, intel, samsung, skhynix
    mdl_nm: Mapped[str] = mapped_column(String(200), index=True, nullable=False) # e.g., RTX 4090, Ryzen 9 7950X, DDR5 32GB PC5-44800
    capa_gb: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True) # 24 (VRAM or RAM capacity)
    
    prc_amt: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    crncy_cd: Mapped[str] = mapped_column(String(10), nullable=False, default="KRW") # KRW, USD
    
    prd_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_offc: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False) # True if MSRP or official foundry price
    
    ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )

    __table_args__ = (
        Index(
            "idx_rtl_prc_hw_mdl_ts",
            "hw_typ", "mdl_nm", "ts",
        ),
        Index(
            "idx_rtl_prc_pltf_mdl_ts",
            "pltf_nm", "mdl_nm", "ts",
        ),
    )

