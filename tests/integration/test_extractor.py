import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from apps.batch.worker.tasks.orchestrator import execute_extraction

async def main():
    await execute_extraction("ncloud")
    await execute_extraction("sugarcube")
    
if __name__ == "__main__":
    asyncio.run(main())
