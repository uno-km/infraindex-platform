from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from apps.api.core.config import settings

if settings.USE_REAL_DB:
    engine = create_async_engine(
        settings.async_database_uri,
        echo=False,
        future=True,
        pool_size=10,
        max_overflow=20,
    )
    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
else:
    engine = None
    AsyncSessionLocal = None

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if not settings.USE_REAL_DB:
        yield None
        return

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
