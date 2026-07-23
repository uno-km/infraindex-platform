import asyncio
import sys
import os

sys.path.append(os.path.abspath('.'))
os.environ['USE_REAL_DB'] = 'True'
import apps.api.main

from apps.api.core.data_service import DataService

async def test():
    print("Testing get_latest_prices...")
    res = await DataService.get_latest_prices()
    print(f"Got {len(res)} prices.")

if __name__ == "__main__":
    asyncio.run(test())
