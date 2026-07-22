import asyncio
import json
from typing import Any
from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.api.core.database import get_db
from apps.api.models.outbox import OutboxEvent

router = APIRouter()

async def event_generator(db: AsyncSession):
    """
    Long-polling generator for Server-Sent Events (SSE).
    In production, this would subscribe to Redis Pub/Sub or Kafka rather than polling Postgres.
    """
    last_id = None
    while True:
        # Check for new outbox events (polling for demonstration of SSE decoupling)
        stmt = select(OutboxEvent).where(OutboxEvent.processed == False).order_by(OutboxEvent.created_at.asc()).limit(10)
        result = await db.execute(stmt)
        events = result.scalars().all()
        
        for event in events:
            # Yield event to the SSE stream
            yield {
                "event": event.event_type,
                "data": json.dumps(event.payload)
            }
            # Mark processed (Simplified for scaffold)
            event.processed = True
            await db.commit()
            
        await asyncio.sleep(1.0) # Poll every 1 second

@router.get("/prices")
async def stream_prices(db: AsyncSession = Depends(get_db)) -> Any:
    """
    Real-time SSE (Server-Sent Events) Gateway for browser clients.
    Connect here to receive live price ticks.
    """
    return EventSourceResponse(event_generator(db))
