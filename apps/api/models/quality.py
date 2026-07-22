from sqlalchemy import String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from apps.api.models.base import Base, UUIDMixin, TimeStampMixin
from datetime import datetime

class CollectionRun(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "collection_runs"
    
    provider_id: Mapped[str] = mapped_column(ForeignKey("providers.id"), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(50)) # success, failed, partial
    items_collected: Mapped[int] = mapped_column(Integer, default=0)
    
class DataQualityIssue(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "data_quality_issues"
    
    observation_id: Mapped[str | None] = mapped_column(ForeignKey("price_observations.id"), index=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("collection_runs.id"), index=True)
    issue_type: Mapped[str] = mapped_column(String(100)) # negative_price, missing_field, extreme_variance
    severity: Mapped[str] = mapped_column(String(50)) # quarantine, warning, info
    description: Mapped[str] = mapped_column(Text)
