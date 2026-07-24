import asyncio
from apps.server.api.v1.endpoints.chart import get_candlestick
async def main():
    print(await get_candlestick('AWS EC2 i3.metal', 90, None))
asyncio.run(main())
