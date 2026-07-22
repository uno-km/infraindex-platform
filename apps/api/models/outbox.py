from sqlalchemy import String, Boolean, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from typing import Dict, Any
from datetime import datetime

from apps.api.models.base import Base, UUIDMixin

class OutboxEvent(Base, UUIDMixin):
    """
    Transactional Outbox Pattern.
    When a domain entity (e.g. PriceObservation) is created/updated, an event is written 
    here within the same DB transaction. A background worker picks it up and pushes it 
    to the EventBus (e.g. Kafka/Redis), ensuring zero data loss and no dual-write bugs.
    """
    __tablename__ = "outbox_events"
    
    topic: Mapped[str] = mapped_column(String(255), index=True)
    event_type: Mapped[str] = mapped_column(String(255))
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    processed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
