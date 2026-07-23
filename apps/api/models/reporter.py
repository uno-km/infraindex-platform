import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Date, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from apps.api.models.base import Base

class DailyReport(Base):
    __tablename__ = "tbl_daily_report"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_date = Column(Date, nullable=False, index=True)
    report_type = Column(String(20), nullable=False) # "morning", "evening"
    file_path = Column(String, nullable=False)
    file_size_bytes = Column(Integer, default=0)
    generated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("report_date", "report_type", name="uq_daily_report_date_type"),
    )
