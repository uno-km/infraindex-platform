from sqlalchemy import String, Boolean, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from typing import Dict, Any
from datetime import datetime

from apps.api.models.base import Base, UUIDMixin

class OutboxEvent(Base, UUIDMixin):
    """
    Transactional Outbox Pattern.
    - tbl_obx_evt
    """
    __tablename__ = "tbl_obx_evt"
    
    tpc_nm: Mapped[str] = mapped_column(String(255), index=True)
    evt_typ: Mapped[str] = mapped_column(String(255))
    payld_dat: Mapped[Dict[str, Any]] = mapped_column(JSON)
    crt_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    proc_st: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    proc_ts: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

