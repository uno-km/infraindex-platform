# -*- coding: utf-8 -*-
import sys
with open('run_full_pipeline.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

header = """import asyncio
import json
import sys
import time
import urllib.request
from datetime import datetime
import os

from scripts.migrate_json_to_db import migrate_json_to_db
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from apps.server.core.data_service import get_chart_data, get_insights

async def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    OUTPUT_DIR = "data/crawled"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
"""

footer = """
    # --- PRE-COMPUTATION & CACHE INVALIDATION ---
    print("\\n=== 시작: DB 마이그레이션 및 캐시 갱신 ===")
    try:
        # 1. DB에 저장 (migrate_json_to_db.py)
        await migrate_json_to_db()
        print("  DB 마이그레이션 완료")
        
        # 2. Redis 캐시 무효화 및 사전 연산 (Pre-computation)
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
        redis_client = aioredis.from_url(redis_url)
        FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
        
        # FastAPI-Cache를 통째로 비우는 방법:
        await FastAPICache.clear()
        print("  Redis 전체 캐시 Flush 완료")
        
        # 3. 사전 연산 (API 서버 대신 미리 연산하여 캐시에 적재)
        from shared.db.session import AsyncSessionLocal
        async with AsyncSessionLocal() as session:
            await get_chart_data(session=session, provider="all", gpu_model="all", days=90)
            await get_chart_data(session=session, provider="aws", gpu_model="A100", days=90)
            await get_insights(session=session, timeframe="1mo")
        print("  차트/인사이트 사전 연산(Pre-computation) 완료 -> Redis 적재 성공")
        
    except Exception as e:
        print(f"  캐시 갱신 실패: {e}")

if __name__ == "__main__":
    asyncio.run(main())
"""

filtered_lines = []
skip_mode = True
for line in lines:
    if skip_mode:
        if "timestamp = " in line:
            skip_mode = False
        else:
            continue
    
    if line.strip() == '':
        filtered_lines.append('\n')
    else:
        filtered_lines.append('    ' + line)

with open('run_full_pipeline.py', 'w', encoding='utf-8') as f:
    f.write(header + ''.join(filtered_lines) + footer)
