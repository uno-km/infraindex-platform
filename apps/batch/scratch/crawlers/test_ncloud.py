import asyncio, sys, logging
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
logging.basicConfig(level=logging.INFO, format='%(message)s')
from apps.batch.services.gpu.crawler_korean_real import crawl_ncloud

r = asyncio.run(crawl_ncloud())
print(f'\n=== NCloud 결과: {len(r)}건 ===')
for x in r[:20]:
    sc = x.get('server_code', '?')
    model = x.get('gpu_model', '?')
    vram = x.get('vram_gb', 0)
    krw = x.get('hourly_krw', 0)
    usd = x.get('price_per_hour', 0)
    print(f'  {sc:25s} | {model:6s} | {vram}GB | {krw:,}원/hr | ${usd}')
