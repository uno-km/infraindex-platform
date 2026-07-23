import asyncio
from apps.api.core.database import _build_engine
from sqlalchemy import text
async def main():
    engine = _build_engine()
    async with engine.begin() as conn:
        await conn.execute(text('TRUNCATE TABLE tbl_news_arti CASCADE'))
    await engine.dispose()
asyncio.run(main())
