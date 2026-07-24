import asyncio
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from apps.server.core.security import get_password_hash
from shared.config.settings import settings

async def seed_admin():
    db_url = settings.async_database_uri

    engine = create_async_engine(db_url, echo=True)

    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT id FROM user_bas WHERE email = 'admin'"))
        admin_id = result.scalar_one_or_none()
        
        hashed = get_password_hash("1234")
        if not admin_id:
            await conn.execute(text(
                "INSERT INTO user_bas (id, email, nickname, hashed_password, is_admin, is_active, created_at) "
                "VALUES (gen_random_uuid(), 'admin', '어드민', :hashed, true, true, now())"
            ), {"hashed": hashed})
            print("Admin user created successfully.")
        else:
            await conn.execute(text(
                "UPDATE user_bas SET hashed_password = :hashed, nickname = '어드민' WHERE email = 'admin'"
            ), {"hashed": hashed})
            print("Admin user already exists. Password and nickname updated.")
            
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed_admin())
