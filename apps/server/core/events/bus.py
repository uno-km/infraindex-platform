from abc import ABC, abstractmethod
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from shared.models.outbox import OutboxEvent

class EventBus(ABC):
    @abstractmethod
    async def publish(self, topic: str, event_type: str, payload: Dict[str, Any], session: AsyncSession) -> None:
        """Publishes an event."""
        pass

class PostgresOutboxEventBus(EventBus):
    """
    Implements the Outbox pattern. Events are written to the 'outbox_events' table 
    within the same Postgres transaction as the domain entity update.
    """
    async def publish(self, topic: str, event_type: str, payload: Dict[str, Any], session: AsyncSession) -> None:
        event = OutboxEvent(
            topic=topic,
            event_type=event_type,
            payload=payload
        )
        session.add(event)
        # Flush to ensure it's part of the current transaction, but we don't commit here.
        # The caller (domain service) commits the entire transaction.
        await session.flush()

# Dependency injection token
event_bus = PostgresOutboxEventBus()
