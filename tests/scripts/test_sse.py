import asyncio
import httpx
from apps.api.core.database import AsyncSessionLocal
from apps.api.models.outbox import OutboxEvent

async def fire_event():
    # Insert a dummy event into the DB to trigger the SSE stream
    async with AsyncSessionLocal() as db:
        event = OutboxEvent(
            topic="prices",
            event_type="PriceChanged",
            payload={"gpu_model": "H100", "provider": "Vast.ai", "new_price": 1.75}
        )
        db.add(event)
        await db.commit()
        print("Fired PriceChanged event into Outbox.")

async def listen_sse():
    print("Listening to SSE on http://localhost:8000/api/v1/stream/prices ...")
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream("GET", "http://localhost:8000/api/v1/stream/prices") as response:
                async for line in response.aiter_lines():
                    if line:
                        print(f"SSE Received: {line}")
                        if "PriceChanged" in line:
                            break # exit when we get the event
        except Exception as e:
            print(f"Could not connect to SSE stream: {e}")

async def main():
    # Start listening in background
    listener = asyncio.create_task(listen_sse())
    
    # Wait a sec then fire event
    await asyncio.sleep(2)
    await fire_event()
    
    # Wait for listener to receive it
    await listener

if __name__ == "__main__":
    asyncio.run(main())
