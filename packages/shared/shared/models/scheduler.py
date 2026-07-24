from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from shared.models.base import Base, UUIDMixin, TimeStampMixin
from typing import Optional
from datetime import datetime

class ScheduleConfig(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "schedule_configs"
    provider_id: Mapped[str] = mapped_column(String(255), index=True)
    cron_expression: Mapped[str] = mapped_column(String(50)) # e.g. "0 9,13,18 * * *"
    timezone: Mapped[str] = mapped_column(String(50), default="Asia/Seoul")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)

class IdempotencyKey(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "idempotency_keys"
    key: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    job_name: Mapped[str] = mapped_column(String(255))
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
