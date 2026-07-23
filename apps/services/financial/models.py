import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from apps.api.models.base import Base, UUIDMixin

class FinMktHistory(Base, UUIDMixin):
    """
    금융/주식/선물 시장 시세 이력 테이블.
    - tbl_fin_mkt_hist
    """
    __tablename__ = "tbl_fin_mkt_hist"

    ast_typ: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # "stock", "future"
    sym_cd: Mapped[str] = mapped_column(String(100), nullable=False, index=True)      # e.g., "NVDA", "DRAM_FUTURES"
    
    opn_prc: Mapped[float] = mapped_column(Float, nullable=False)
    hi_prc: Mapped[float] = mapped_column(Float, nullable=False)
    lo_prc: Mapped[float] = mapped_column(Float, nullable=False)
    cls_prc: Mapped[float] = mapped_column(Float, nullable=False)
    vol_cnt: Mapped[float | None] = mapped_column(Float, nullable=True)  # Volume might be null for some indices/futures
    
    crncy_cd: Mapped[str] = mapped_column(String(10), nullable=False, default="USD") # USD, KRW
    ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )
    
    __table_args__ = (
        Index(
            "idx_fin_mkt_sym_ts",
            "sym_cd", "ts",
        ),
    )

