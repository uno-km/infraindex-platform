import asyncio
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
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    all_gpu_data = []
    summary = {}

    # ============================================================
    # 1. RunPod (GraphQL - 즉시 동작)
    # ============================================================
    print("\n=== 1. RunPod GraphQL 크롤링 ===")
    try:
        query = json.dumps({"query": "query { gpuTypes { id displayName memoryInGb securePrice communityPrice } }"})
        req = urllib.request.Request(
            'https://api.runpod.io/graphql',
            data=query.encode(),
            headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
        gpu_types = data.get('data', {}).get('gpuTypes', [])

        runpod_results = []
        for g in gpu_types:
            price = g.get('securePrice') or g.get('communityPrice') or 0
            if price and price > 0:
                runpod_results.append({
                    "provider": "runpod",
                    "gpu_model": g.get('displayName', g.get('id')),
                    "vram_gb": g.get('memoryInGb', 0),
                    "price_per_hour": float(price),
                    "availability_status": "available",
                    "provider_link": "https://www.runpod.io/console/gpu-cloud",
                    "collected_at": timestamp
                })

        all_gpu_data.extend(runpod_results)
        summary['runpod'] = len(runpod_results)
        print(f"  RunPod: {len(runpod_results)}건 수집")
        for r in runpod_results[:5]:
            print(f"    {r['gpu_model']}: {r['vram_gb']}GB, ${r['price_per_hour']}/hr")

    except Exception as e:
        print(f"  RunPod 실패: {e}")
        summary['runpod'] = 0


    # ============================================================
    # 2. AWS EC2 Seoul Pricing
    # ============================================================
    print("\n=== 2. AWS EC2 서울 리전 가격 크롤링 ===")
    try:
        url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-northeast-2/index.json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        print("  다운로드 중 (약 300MB, 10~30초)...")
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=90) as r:
            raw = r.read()
        elapsed = time.time() - t0

        data = json.loads(raw)
        products = data.get('products', {})
        terms = data.get('terms', {}).get('OnDemand', {})

        GPU_PREFIXES = ('p4d', 'p4de', 'p3', 'p3dn', 'g5', 'g4dn', 'g4ad', 'trn1', 'inf2', 'g6', 'p5')
        GPU_MAP = {
            'p4d': 'A100', 'p4de': 'A100', 'p3': 'V100', 'p3dn': 'V100',
            'g5': 'A10G', 'g4dn': 'T4', 'g4ad': 'Radeon V520',
            'trn1': 'Trainium', 'inf2': 'Inferentia2',
            'g6': 'L4', 'g6e': 'L40S', 'p5': 'H100', 'p5e': 'H100',
            'g4': 'T4',
        }

        aws_results = []
        seen_instances = set()

        for sku, product in products.items():
            attrs = product.get('attributes', {})
            itype = attrs.get('instanceType', '')

            if not any(itype.startswith(p) for p in GPU_PREFIXES):
                continue
            if attrs.get('operatingSystem', '').lower() != 'linux':
                continue
            if attrs.get('tenancy', '').lower() != 'shared':
                continue
            if itype in seen_instances:
                continue

            sku_terms = terms.get(sku, {})
            price = None
            for offer in sku_terms.values():
                for dim in offer.get('priceDimensions', {}).values():
                    try:
                        p = float(dim.get('pricePerUnit', {}).get('USD', '0'))
                        if p > 0:
                            price = p
                    except:
                        pass

            if price:
                prefix = itype.split('.')[0].lower()
                gpu_name = GPU_MAP.get(prefix, 'Unknown GPU')
                seen_instances.add(itype)

                aws_results.append({
                    "provider": "aws",
                    "gpu_model": gpu_name,
                    "instance_type": itype,
                    "price_per_hour": round(price, 4),
                    "availability_status": "available",
                    "provider_link": f"https://aws.amazon.com/ec2/instance-types/{itype.split('.')[0]}/",
                    "collected_at": timestamp
                })

        all_gpu_data.extend(aws_results)
        summary['aws'] = len(aws_results)
        print(f"  AWS: {len(aws_results)}건 수집 ({len(raw)//1024}KB in {elapsed:.1f}s)")
        for r in aws_results[:5]:
            print(f"    {r['instance_type']} ({r['gpu_model']}): ${r['price_per_hour']}/hr")

    except Exception as e:
        print(f"  AWS 실패: {e}")
        summary['aws'] = 0


    # ============================================================
    # 3. Korean Providers (Playwright 기반)
    # ============================================================
    print("\n=== 3. 한국 GPU 클라우드 크롤링 (Playwright) ===")
    try:
        from apps.batch.services.gpu.crawler_korean_real import run_all_crawlers
        korean_results_by_provider = asyncio.run(run_all_crawlers())

        for provider, items in korean_results_by_provider.items():
            for item in items:
                item['collected_at'] = timestamp
            all_gpu_data.extend(items)
            summary[provider] = len(items)
            print(f"  {provider}: {len(items)}건")

    except Exception as e:
        print(f"  한국 크롤러 실패: {e}")


    # ============================================================
    # 4. 주식/반도체 가격 (Yahoo Finance)
    # ============================================================
    print("\n=== 4. 반도체 주식 가격 (Yahoo Finance) ===")
    STOCK_SYMBOLS = {
        'NVDA': 'NVIDIA Corp',
        'AMD': 'AMD',
        '000660.KS': 'SK하이닉스',
        '005930.KS': '삼성전자',
        'WDC': 'Western Digital',
        'INTC': 'Intel',
        'MU': '마이크론',
        'TSM': 'TSMC',
        'AMAT': 'Applied Materials',
    }

    stock_results = []
    for sym, name in STOCK_SYMBOLS.items():
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1d"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
            chart = data.get('chart', {}).get('result', [{}])
            if chart:
                meta = chart[0].get('meta', {})
                price = meta.get('regularMarketPrice', 0)
                prev = meta.get('chartPreviousClose', 0)
                currency = meta.get('currency', '?')
                change_pct = ((price - prev) / prev * 100) if prev else 0
                stock_results.append({
                    "symbol": sym,
                    "company": name,
                    "price": price,
                    "prev_close": prev,
                    "change_pct": round(change_pct, 2),
                    "currency": currency,
                    "collected_at": timestamp
                })
                print(f"  {sym} ({name}): {currency} {price:,.2f} ({change_pct:+.2f}%)")
        except Exception as e:
            print(f"  {sym}: 실패 - {e}")

    summary['stocks'] = len(stock_results)


    # ============================================================
    # 5. 뉴스 RSS (Google News)
    # ============================================================
    print("\n=== 5. 반도체/GPU 뉴스 (Google News RSS) ===")
    import re as _re

    NEWS_QUERIES = [
        ('GPU cloud price', 'gpu+cloud+price'),
        ('SK Hynix DRAM HBM', 'SK+Hynix+DRAM+HBM'),
        ('NVIDIA GPU AI', 'NVIDIA+GPU+AI'),
        ('semiconductor memory price', 'semiconductor+memory+price'),
        ('HBM GPU DRAM Korea', 'HBM+GPU+DRAM+Korea'),
    ]

    news_results = []
    for name, q in NEWS_QUERIES:
        try:
            url = f"https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as r:
                content = r.read().decode('utf-8', errors='ignore')

            # RSS 파싱
            items = _re.findall(r'<item>(.*?)</item>', content, _re.DOTALL)
            for item_xml in items[:10]:
                title_m = _re.search(r'<title>(.*?)</title>', item_xml)
                link_m = _re.search(r'<link>(.*?)</link>', item_xml)
                pub_m = _re.search(r'<pubDate>(.*?)</pubDate>', item_xml)
                source_m = _re.search(r'<source[^>]*>(.*?)</source>', item_xml)

                if title_m:
                    title = _re.sub(r'<[^>]+>', '', title_m.group(1))
                    link = link_m.group(1) if link_m else ''
                    pub = pub_m.group(1) if pub_m else ''
                    source = source_m.group(1) if source_m else name

                    news_results.append({
                        "title": title,
                        "url": link,
                        "source": source,
                        "published_at": pub,
                        "query": name,
                        "collected_at": timestamp
                    })

            print(f"  '{name}': {len(items)}건")
        except Exception as e:
            print(f"  '{name}' 실패: {e}")

    summary['news'] = len(news_results)


    # ============================================================
    # 저장
    # ============================================================
    print("\n=== 수집 결과 저장 ===")

    # GPU 데이터
    gpu_file = f"{OUTPUT_DIR}/gpu_prices_{timestamp}.json"
    with open(gpu_file, 'w', encoding='utf-8') as f:
        json.dump(all_gpu_data, f, ensure_ascii=False, indent=2)
    print(f"  GPU 데이터: {gpu_file} ({len(all_gpu_data)}건)")

    # 주식 데이터
    stock_file = f"{OUTPUT_DIR}/stock_prices_{timestamp}.json"
    with open(stock_file, 'w', encoding='utf-8') as f:
        json.dump(stock_results, f, ensure_ascii=False, indent=2)
    print(f"  주식 데이터: {stock_file} ({len(stock_results)}건)")

    # 뉴스 데이터
    news_file = f"{OUTPUT_DIR}/news_{timestamp}.json"
    with open(news_file, 'w', encoding='utf-8') as f:
        json.dump(news_results, f, ensure_ascii=False, indent=2)
    print(f"  뉴스 데이터: {news_file} ({len(news_results)}건)")

    # 요약
    print("\n=== 최종 수집 요약 ===")
    total = sum(v for k, v in summary.items() if k != 'news' and k != 'stocks')
    for k, v in summary.items():
        print(f"  {k}: {v}건")
    print(f"\n  GPU 총합: {total}건")
    print(f"  전체 합계: {sum(summary.values())}건")
    print("\n완료!")

    # --- PRE-COMPUTATION & CACHE INVALIDATION ---
    print("\n=== 시작: DB 마이그레이션 및 캐시 갱신 ===")
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
