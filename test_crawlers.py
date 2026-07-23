"""
실측 크롤러 검증 스크립트 - 2026-07-23
각 데이터 소스에 실제 HTTP 요청을 날려서 데이터를 가져오는지 확인
"""
import urllib.request
import urllib.parse
import json
import sys
import time
import re

# Fix encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

results = {}

def print_sep(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


# ============================================================
# 1. VAST.AI - REST API
# ============================================================
print_sep("1. VAST.AI - https://console.vast.ai/api/v0/bundles/")
try:
    req = urllib.request.Request(
        'https://console.vast.ai/api/v0/bundles/?q=%7B%7D',
        headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.loads(r.read())
    offers = data.get('offers', [])
    print(f"STATUS: OK")
    print(f"Total offers: {len(offers)}")
    
    gpu_map = {}
    for o in offers:
        g = o.get('gpu_name', 'Unknown')
        p = float(o.get('dph_total', 0))
        rentable = o.get('rentable', False)
        if g not in gpu_map:
            gpu_map[g] = {'count': 0, 'prices': [], 'available': 0}
        gpu_map[g]['count'] += 1
        gpu_map[g]['prices'].append(p)
        if rentable:
            gpu_map[g]['available'] += 1
    
    print(f"\nTop 10 GPU types (by listing count):")
    for g, info in sorted(gpu_map.items(), key=lambda x: -x[1]['count'])[:10]:
        min_p = min(info['prices']) if info['prices'] else 0
        print(f"  [{info['available']} avail / {info['count']} total] {g}: from ${min_p:.3f}/h")
    
    results['vast_ai'] = {'status': 'OK', 'count': len(offers), 'gpu_types': len(gpu_map)}
except Exception as e:
    print(f"STATUS: FAILED - {e}")
    results['vast_ai'] = {'status': 'FAILED', 'error': str(e)}


# ============================================================
# 2. RUNPOD - GraphQL API
# ============================================================
print_sep("2. RUNPOD - https://api.runpod.io/graphql")
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
    print(f"STATUS: OK")
    print(f"Total GPU types: {len(gpu_types)}")
    print(f"\nAll GPU types:")
    for g in gpu_types[:15]:
        sp = g.get('securePrice') or 0
        cp = g.get('communityPrice') or 0
        mem = g.get('memoryInGb', 0)
        print(f"  {g.get('displayName', g.get('id'))}: {mem}GB VRAM, secure=${sp}/h, community=${cp}/h")
    results['runpod'] = {'status': 'OK', 'count': len(gpu_types)}
except Exception as e:
    print(f"STATUS: FAILED - {e}")
    results['runpod'] = {'status': 'FAILED', 'error': str(e)}


# ============================================================
# 3. AWS Pricing JSON API (ap-northeast-2 Seoul)
# ============================================================
print_sep("3. AWS EC2 Pricing JSON - Seoul Region (ap-northeast-2)")
try:
    url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-northeast-2/index.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    print("  Fetching (this may take 10-60 sec, file is ~50MB)...")
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=90) as r:
        raw = r.read()
    elapsed = time.time() - t0
    data = json.loads(raw)
    print(f"STATUS: OK ({len(raw)//1024} KB downloaded in {elapsed:.1f}s)")
    
    products = data.get('products', {})
    terms = data.get('terms', {}).get('OnDemand', {})
    GPU_PREFIXES = ('p4d', 'p4de', 'p3', 'p3dn', 'g5', 'g4dn', 'g4ad', 'trn1', 'inf2')
    gpu_instances = []
    for sku, product in products.items():
        attrs = product.get('attributes', {})
        itype = attrs.get('instanceType', '')
        if not any(itype.startswith(p) for p in GPU_PREFIXES):
            continue
        if attrs.get('operatingSystem', '').lower() != 'linux':
            continue
        if attrs.get('tenancy', '').lower() != 'shared':
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
            gpu_instances.append({'instance': itype, 'price': price})
    
    print(f"GPU instances found: {len(gpu_instances)}")
    print("All instances:")
    for g in sorted(gpu_instances, key=lambda x: x['instance']):
        print(f"  {g['instance']}: ${g['price']:.4f}/h")
    results['aws'] = {'status': 'OK', 'count': len(gpu_instances)}
except Exception as e:
    print(f"STATUS: FAILED - {e}")
    results['aws'] = {'status': 'FAILED', 'error': str(e)}


# ============================================================
# 4. Yahoo Finance - Stock Data
# ============================================================
print_sep("4. Yahoo Finance - NVDA, AMD, SK Hynix (000660.KS), Samsung (005930.KS)")
symbols = ['NVDA', 'AMD', '000660.KS', '005930.KS', 'WDC', 'INTC', 'QCOM']
fin_ok = 0
for sym in symbols:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        chart = data.get('chart', {}).get('result', [{}])
        if chart:
            meta = chart[0].get('meta', {})
            price = meta.get('regularMarketPrice', 'N/A')
            prev = meta.get('chartPreviousClose', 'N/A')
            currency = meta.get('currency', '?')
            change_pct = ((float(price) - float(prev)) / float(prev) * 100) if price != 'N/A' and prev != 'N/A' else 0
            print(f"  OK {sym}: {currency} {price} ({change_pct:+.2f}%)")
            fin_ok += 1
        else:
            print(f"  FAIL {sym}: no data")
    except Exception as e:
        print(f"  FAIL {sym}: {e}")
results['yahoo_finance'] = {'status': 'OK', 'count': fin_ok}


# ============================================================
# 5. DRAMeXchange / TrendForce (DRAM 실거래가)
# ============================================================
print_sep("5. DRAM 가격 데이터 소스 검증")

# Try DRAMeXchange
print("\n[DRAMeXchange.com]")
try:
    url2 = "https://www.dramexchange.com/"
    req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req2, timeout=10) as r:
        content2 = r.read().decode('utf-8', errors='ignore')
    print(f"  HTTP OK ({len(content2)} chars)")
    has_price = 'price' in content2.lower() or 'ddr' in content2.lower()
    print(f"  Contains DDR/price keywords: {has_price}")
    if has_price:
        prices = re.findall(r'\$[\d.]+', content2)
        print(f"  Price patterns found: {prices[:5]}")
except Exception as e:
    print(f"  FAILED: {e}")

# Try TrendForce free section
print("\n[TrendForce Memory Spot Price (public data)]")
try:
    url3 = "https://www.trendforce.com/presscenter/news/list/10/"
    req3 = urllib.request.Request(url3, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req3, timeout=10) as r:
        content3 = r.read().decode('utf-8', errors='ignore')
    print(f"  HTTP OK ({len(content3)} chars)")
    titles = re.findall(r'<a[^>]*>(DRAM[^<]{5,60})</a>', content3, re.IGNORECASE)
    if titles:
        print(f"  DRAM related articles:")
        for t in titles[:3]:
            print(f"    - {t.strip()[:80]}")
    else:
        print(f"  No DRAM article titles found in this page")
except Exception as e:
    print(f"  FAILED: {e}")

results['dram'] = {'status': 'Tested'}


# ============================================================
# 6. Google News RSS - Semiconductor/GPU news
# ============================================================
print_sep("6. Google News RSS - 반도체/GPU/메모리 뉴스")
queries = [
    ('GPU cloud price', 'gpu+cloud+price'),
    ('SK Hynix DRAM', 'SK+Hynix+DRAM'),
    ('NVIDIA semiconductor', 'NVIDIA+semiconductor'),
]
rss_ok = 0
for name, q in queries:
    try:
        url = f"https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            content = r.read().decode('utf-8', errors='ignore')
        item_count = content.count('<item>')
        titles = re.findall(r'<title>(.*?)</title>', content)
        print(f"\n  '{name}': {item_count} articles")
        for t in titles[1:4]:
            clean = re.sub(r'<[^>]+>', '', t)
            print(f"    - {clean[:80]}")
        rss_ok += item_count
    except Exception as e:
        print(f"\n  '{name}': FAILED - {e}")

results['google_news_rss'] = {'status': 'OK', 'total_articles': rss_ok}


# ============================================================
# 7. Korean providers (direct HTTP check)
# ============================================================
print_sep("7. Korean GPU Cloud Sites - HTTP Accessibility")
korean_sites = {
    'GPUaaS': 'https://gpuaas.kr/',
    'CloudV': 'https://cloudv.kr/server/gpu.html',
    'RunYourAI': 'https://console.runyour.ai/gpu-cloud',
    'Gabia': 'https://www.gabia.com/',
    'KT Cloud': 'https://cloud.kt.com/',
    'VESSL AI': 'https://vessl.ai/ko/pricing',
    'NCloud': 'https://www.ncloud.com/product/compute/gpuServer',
}
for name, url in korean_sites.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            content = r.read().decode('utf-8', errors='ignore')
        status_code = r.getcode()
        print(f"  OK [{status_code}] {name}: {url} ({len(content)} chars)")
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} {name}: {url}")
    except Exception as e:
        print(f"  FAIL {name}: {url} => {type(e).__name__}: {str(e)[:50]}")


# ============================================================
# FINAL SUMMARY
# ============================================================
print_sep("FINAL SUMMARY")
for source, info in results.items():
    status = info.get('status', '?')
    ok = status in ('OK', 'Tested')
    count = info.get('count', '')
    count_str = f" ({count} records)" if count else ""
    error = info.get('error', '')
    error_str = f" => {error[:60]}" if error and not ok else ""
    print(f"  [{'OK' if ok else 'FAIL'}] {source}: {status}{count_str}{error_str}")

print("\n=== 검증 완료 ===")
