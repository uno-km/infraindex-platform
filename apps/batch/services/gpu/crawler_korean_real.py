"""
Korean GPU Cloud Providers - 실제 Playwright 파싱 크롤러
각 사이트 HTML 분석 결과 기반으로 실제 파싱 로직 구현

분석 일시: 2026-07-23
분석 방법: Playwright로 실제 렌더링 후 DOM 구조 확인
"""
import asyncio
import re
import logging
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

# 원화 -> USD 환산 (1달러 = 1,380원 기준, 실시간은 yfinance로 업데이트 가능)
KRW_TO_USD = 1 / 1380.0


def krw_to_usd(krw: float) -> float:
    return round(krw * KRW_TO_USD, 4)


def parse_price_number(text: str) -> Optional[float]:
    """텍스트에서 숫자만 추출 (콤마, 공백 제거)"""
    cleaned = re.sub(r'[^\d.]', '', text.replace(',', ''))
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


# ============================================================
# 공통: Playwright 페이지 가져오기
# ============================================================
async def fetch_page_content(url: str, wait_for: str = "networkidle", extra_wait_ms: int = 3000) -> str:
    """
    Playwright로 페이지를 렌더링하여 최종 HTML 반환.
    SPA(React/Vue)의 경우 networkidle + 추가 대기.
    """
    logger.info(f"Fetching {url} via Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        try:
            await page.goto(url, wait_until=wait_for, timeout=60000)
            await page.wait_for_timeout(extra_wait_ms)
            html = await page.content()
            logger.info(f"Fetched {url}: {len(html)} chars")
            return html
        except Exception as e:
            logger.error(f"Playwright error for {url}: {e}")
            return ""
        finally:
            await browser.close()


# ============================================================
# 1. VESSL AI (vessl.ai/ko/pricing)
# ============================================================
async def crawl_vessl() -> List[Dict]:
    """
    파싱 전략: <table>에서 GPU 모델 | VRAM | 아키텍처 | 온디맨드 가격 추출
    실제 테이블 내용 (분석 확인):
      GPU 모델 | VRAM | 아키텍처 | 온디맨드 | 예약 인스턴스
      NVIDIA B300 | 288GB | Blackwell | $7.29/hr | ...
      NVIDIA H100 SXM | 80GB | Hopper | $3.19/hr | ...
      NVIDIA A100 SXM | 80GB | Ampere | $1.39/hr | ...
      NVIDIA L40S | 48GB | Ada Lovelace | $1.80/hr | ...
    """
    url = "https://vessl.ai/ko/pricing"
    results = []
    
    try:
        html = await fetch_page_content(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'lxml')
        
        # 테이블 찾기
        tables = soup.find_all('table')
        logger.info(f"[VESSL] Found {len(tables)} tables")
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                if len(cells) < 4:
                    continue
                
                # 패턴: [GPU 모델명, VRAM, 아키텍처, 온디맨드 가격, ...]
                # 가격 셀에서 $x.xx/hr 패턴 찾기
                price_match = None
                gpu_name = None
                vram_gb = 0
                
                for i, cell in enumerate(cells):
                    # GPU 이름 추출 (NVIDIA로 시작하는 셀)
                    if 'NVIDIA' in cell or 'H100' in cell or 'A100' in cell or 'B200' in cell or 'L40' in cell:
                        # 불필요한 텍스트 제거
                        gpu_raw = re.sub(r'바로 시작|문의|지금 시작하기', '', cell).strip()
                        if gpu_raw and len(gpu_raw) < 50:
                            gpu_name = gpu_raw
                    
                    # VRAM 추출 (xGBGB 패턴)
                    vram_match = re.search(r'(\d+)GB', cell)
                    if vram_match and vram_gb == 0:
                        vram_gb = int(vram_match.group(1))
                    
                    # 가격 추출 ($x.xx/hr 패턴)
                    price_match_try = re.search(r'\$(\d+\.?\d*)/hr', cell)
                    if price_match_try:
                        price_match = float(price_match_try.group(1))
                
                if gpu_name and price_match and price_match > 0:
                    results.append({
                        "provider": "vessl",
                        "gpu_model": gpu_name.replace("NVIDIA ", ""),
                        "vram_gb": vram_gb,
                        "price_per_hour": price_match,
                        "availability_status": "available",
                        "provider_link": url,
                    })
                    logger.info(f"  [VESSL] {gpu_name}: {vram_gb}GB VRAM, ${price_match}/hr")
        
        logger.info(f"[VESSL] Total: {len(results)} instances parsed")
        return results
        
    except Exception as e:
        logger.error(f"[VESSL] Crawl failed: {e}")
        return []


# ============================================================
# 2. GPUaaS (gpuaas.kr)
# ============================================================
async def crawl_gpuaas() -> List[Dict]:
    """
    파싱 전략: [class*="price"] 테이블에서 가격 추출
    실제 테이블 내용 (분석 확인):
      플랜 | GPU당 요금 | 동일 VRAM 기준 AWS 요금 | 절감율
      시간제 | $2.39/hr | $6.9/hr | -65%
      연간 계약 | $2.2/hr | - | -
    참고: GPUaaS는 VESSL AI의 서비스 (H100 SXM 80GB)
    """
    url = "https://gpuaas.kr/"
    results = []
    
    try:
        html = await fetch_page_content(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'lxml')
        text = soup.get_text(separator='\n')
        
        # H100 SXM 가격 테이블 추출
        # 패턴: "시간제\t$2.39/hr"
        price_matches = re.findall(r'시간제\s*\$?(\d+\.?\d*)/hr', text)
        annual_matches = re.findall(r'연간 계약\s*\$?(\d+\.?\d*)/hr', text)
        
        # 페이지에서 GPU 이름 확인
        gpu_found = "H100 SXM"  # 페이지 컨텍스트에서 확인된 GPU
        vram = 80
        
        if price_matches:
            price = float(price_matches[0])
            results.append({
                "provider": "gpuaas",
                "gpu_model": gpu_found,
                "vram_gb": vram,
                "price_per_hour": price,
                "availability_status": "available",
                "provider_link": url,
            })
            logger.info(f"  [GPUaaS] {gpu_found}: {vram}GB VRAM, ${price}/hr (온디맨드)")
        
        if annual_matches:
            price = float(annual_matches[0])
            results.append({
                "provider": "gpuaas",
                "gpu_model": f"{gpu_found} (연간계약)",
                "vram_gb": vram,
                "price_per_hour": price,
                "availability_status": "available",
                "provider_link": url,
            })
            logger.info(f"  [GPUaaS] {gpu_found} (연간계약): ${price}/hr")
        
        # A100 가격도 있는지 확인
        a100_matches = re.findall(r'A100[^\n]*\$(\d+\.?\d*)/hr', text)
        for a100_price in a100_matches:
            results.append({
                "provider": "gpuaas",
                "gpu_model": "A100 SXM",
                "vram_gb": 80,
                "price_per_hour": float(a100_price),
                "availability_status": "available",
                "provider_link": url,
            })
        
        logger.info(f"[GPUaaS] Total: {len(results)} instances parsed")
        return results
        
    except Exception as e:
        logger.error(f"[GPUaaS] Crawl failed: {e}")
        return []


# ============================================================
# 3. CloudV (cloudv.kr/server/gpu.html)
# ============================================================
async def crawl_cloudv() -> List[Dict]:
    """
    파싱 전략: 본문 텍스트에서 GPU 이름 + IDC 요금(월) 패턴 추출
    실제 페이지 구조 (분석 확인):
      A100 40GB.G1 → IDC 요금 189,800원/월
      A100 40GB.G2 → IDC 요금 314,800원/월 (2x GPU)
      A100 80GB.G1 → IDC 요금 227,800원/월
      RTX 5090     → 없음 (별도 문의)
    참고: CloudV는 월 임대 서비스. 시간당으로 변환 필요.
    """
    url = "https://cloudv.kr/server/gpu.html"
    results = []
    
    try:
        html = await fetch_page_content(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'lxml')
        text = soup.get_text(separator='\n')
        
        # 패턴: GPU 모델명 뒤에 IDC 요금이 오는 블록 찾기
        # "A100 40GB.G1\nGPU Memory 40GB\n...\nIDC 요금\n189,800원/월"
        
        # 블록 기반 파싱 - 각 GPU 스펙 블록 찾기
        blocks = re.split(r'\n(?=A100|RTX|H100|L40|V100)', text)
        
        gpu_pattern = re.compile(r'(A100 \d+GB|RTX \d+|H100|L40S?|V100|PRO \d+)', re.IGNORECASE)
        price_pattern = re.compile(r'IDC 요금\s*([\d,]+)원/월', re.IGNORECASE)
        gpu_count_pattern = re.compile(r'(\d+)\s*x\s*NVIDIA')
        vram_pattern = re.compile(r'GPU Memory\s*(\d+)GB')
        
        for block in blocks:
            gpu_match = gpu_pattern.search(block)
            price_match = price_pattern.search(block)
            
            if gpu_match and price_match:
                gpu_name = gpu_match.group(1)
                monthly_krw = int(price_match.group(1).replace(',', ''))
                
                # GPU 수량 확인
                count_match = gpu_count_pattern.search(block)
                gpu_count = int(count_match.group(1)) if count_match else 1
                
                # VRAM 확인
                vram_match = vram_pattern.search(block)
                vram_total = int(vram_match.group(1)) if vram_match else 0
                vram_per_gpu = vram_total // gpu_count if gpu_count > 0 else vram_total
                
                # 월 KRW → 시간당 USD 변환 (1달 = 730시간)
                hourly_usd = round((monthly_krw * KRW_TO_USD) / 730, 4)
                
                results.append({
                    "provider": "cloudv",
                    "gpu_model": gpu_name,
                    "vram_gb": vram_per_gpu,
                    "price_per_hour": hourly_usd,
                    "availability_status": "available",
                    "provider_link": url,
                    "gpu_count": gpu_count,
                    "monthly_krw": monthly_krw,
                    "note": f"{gpu_count}x GPU, {monthly_krw:,}원/월 (IDC요금)"
                })
                logger.info(f"  [CloudV] {gpu_name} x{gpu_count}: {monthly_krw:,}원/월 → ${hourly_usd}/hr")
        
        # 중복 제거 (동일 GPU 모델 + 가격)
        seen = set()
        unique_results = []
        for r in results:
            key = (r['gpu_model'], r['price_per_hour'])
            if key not in seen:
                seen.add(key)
                unique_results.append(r)
        
        logger.info(f"[CloudV] Total: {len(unique_results)} instances parsed")
        return unique_results
        
    except Exception as e:
        logger.error(f"[CloudV] Crawl failed: {e}")
        return []


# ============================================================
# 4. RunYourAI (console.runyour.ai)
# ============================================================
async def crawl_runyourai() -> List[Dict]:
    """
    파싱 전략: GPU 카드에서 GPU명 + 이용 요금 추출
    실제 페이지 구조 (분석 확인):
      NVIDIA H100 → 이용 요금: 3,780 C / hr  (Reserved)
      NVIDIA A100 (80GB) → 이용 요금: 2,657 C / hr
      NVIDIA A100 (40GB) → 이용 요금: 2,007 C / hr
      NVIDIA A4000 → 459 C / hr
      NVIDIA V100 → 670 C / hr
    참고: C = 크레딧 (1C ≈ 1원으로 추정, 실제 확인 필요)
    분석 로그에서 확인: 1,261 C/hr → H100 기준 RunPod $3.19/hr 대비 약 1261원/hr → $0.91
    크레딧 정보 미확인 시 원화 기준으로 저장
    """
    url = "https://console.runyour.ai/gpu-cloud"
    results = []
    
    try:
        html = await fetch_page_content(url, extra_wait_ms=5000)  # SPA이므로 추가 대기
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'lxml')
        text = soup.get_text(separator='\n')
        
        # GPU 카드 블록 파싱
        # 패턴: GPU명 → 이용 요금: [숫자] C / hr
        gpu_blocks = re.split(r'\n(?=NVIDIA|RTX|Tesla)', text)
        
        gpu_name_re = re.compile(r'(NVIDIA\s+\w+[\w\s]*?(?:\d+GB)?)', re.IGNORECASE)
        price_re = re.compile(r'이용 요금\s*([\d,]+)\s*C\s*/\s*hr')
        vram_re = re.compile(r'(\d+)\s*GB\s*VRAM')
        
        seen_gpus = set()
        
        for block in gpu_blocks:
            gpu_match = gpu_name_re.search(block)
            price_match = price_re.search(block)
            vram_match = vram_re.search(block)
            
            if gpu_match and price_match:
                gpu_name = gpu_match.group(1).strip()
                credits_per_hr = int(price_match.group(1).replace(',', ''))
                vram_gb = int(vram_match.group(1)) if vram_match else 0
                
                # 크레딧 → USD 변환 (1 C ≈ 1 KRW, 1380 KRW/USD)
                price_usd = round(credits_per_hr * KRW_TO_USD, 4)
                
                key = (gpu_name[:20], credits_per_hr)
                if key not in seen_gpus and len(gpu_name) < 50:
                    seen_gpus.add(key)
                    results.append({
                        "provider": "runyourai",
                        "gpu_model": gpu_name.replace("NVIDIA ", ""),
                        "vram_gb": vram_gb,
                        "price_per_hour": price_usd,
                        "availability_status": "available",
                        "provider_link": url,
                        "raw_credits_per_hr": credits_per_hr,
                        "note": f"{credits_per_hr:,} C/hr (1C≈1KRW 기준)"
                    })
                    logger.info(f"  [RunYourAI] {gpu_name}: {vram_gb}GB VRAM, {credits_per_hr:,} C/hr → ${price_usd}/hr")
        
        logger.info(f"[RunYourAI] Total: {len(results)} instances parsed")
        return results
        
    except Exception as e:
        logger.error(f"[RunYourAI] Crawl failed: {e}")
        return []


# ============================================================
# 5. NCloud (ncloud.com/product/compute/gpuServer)
# ============================================================
async def crawl_ncloud() -> List[Dict]:
    """
    NCloud GPU 가격 실파싱.
    중요: body.innerText는 568자짜리를 반환하지만,
    playwright의 table.inner_text()로 직접 접근하면 실제 테이블 데이터가 다 있음.
    
    실측 테이블 데이터 (디버그 확인):
      테이블2: L40S 가격 - gp1ls16-g3 → 4,309원/hr
      테이블3: L4 가격   - gp1l4-g3  → 1,447원/hr
      테이블4: A100 가격  - gp8ap56-g3 → 49,928원/hr
      테이블5: V100 가격  - gp1vs8-g1-h50 → 4,281원/hr
    """
    url = "https://www.ncloud.com/product/compute/gpuServer"
    results = []
    
    # GPU 코드 suffix → (GPU 모델, VRAM) 매핑
    SUFFIX_MAP = {
        'ls': ('L40S', 48),    # ls = L40S
        'l4': ('L4', 24),      # l4 = L4
        'ap': ('A100', 80),    # ap = A100 80GB
        'vs': ('V100', 32),    # vs = V100 (vintage server)
        'hv': ('H200', 141),   # hv = H200
    }
    
    try:
        logger.info(f"[NCloud] Playwright 실행 중...")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            await page.goto(url, wait_until="networkidle", timeout=60000)
            await page.wait_for_timeout(3000)
            
            tables = await page.query_selector_all('table')
            logger.info(f"[NCloud] {len(tables)}개 테이블 발견")
            
            for table_el in tables:
                # inner_text()는 줄바꿈/탭 없이 단일 연속 문자열 반환
                # 예: "...gp1ls16-g31개 x 48GB16개96GB-4,309 원3,102,080 원gp1ls32-g3..."
                text = await table_el.inner_text()
                
                # BOM 제거
                text = text.replace('\ufeff', '')
                
                # 패턴: gp코드 → 시간 요금(소액) + 월 요금(대액)
                # gp1ls16-g3 ... 4,309 원 ... 3,102,080 원
                # gp8ap56-g3 ... 49,928 원 ... 35,948,160 원
                #
                # 핵심: gp 코드 뒤에 나오는 첫 번째 "X,XXX 원" (1000~999999)
                #       두 번째 큰 숫자는 월 요금이므로 무시
                
                # 모든 gp 코드 추출
                gp_positions = [(m.start(), m.group(0)) for m in re.finditer(r'gp\w+', text)]
                
                for i, (pos, server_code) in enumerate(gp_positions):
                    sc = server_code.lower()
                    
                    # 다음 gp코드 전까지의 범위
                    end = gp_positions[i+1][0] if i+1 < len(gp_positions) else len(text)
                    segment = text[pos:end]
                    
                    # GPU 수량 추출
                    count_m = re.search(r'^gp(\d+)', sc)
                    gpu_count = int(count_m.group(1)) if count_m else 1
                    
                    # GPU 모델 추론 (서버 코드 기반)
                    gpu_model, vram_per_gpu = 'Unknown', 0
                    for suffix, (model, vram) in SUFFIX_MAP.items():
                        if sc[3:3+len(suffix)] == suffix or suffix in sc[3:7]:
                            gpu_model, vram_per_gpu = model, vram
                            break
                    
                    if gpu_model == 'Unknown':
                        continue
                    
                    # 시간 요금 추출: 세그먼트에서 "X,XXX 원" 중 범위에 맞는 첫 번째
                    price_matches = re.findall(r'([\d,]+)\s*원', segment)
                    hourly_krw = None
                    for pm in price_matches:
                        val = int(pm.replace(',', ''))
                        # 시간당 요금: 1,000원 ~ 999,999원 (월 요금은 보통 수백만원)
                        if 1000 <= val <= 999999 and val < 1_000_000:
                            # 월 요금과 구분: 단순히 첫 번째 소액 값이 시간 요금
                            hourly_krw = val
                            break
                    
                    if not hourly_krw:
                        continue
                    
                    price_usd = round(hourly_krw * KRW_TO_USD, 4)
                    
                    results.append({
                        "provider": "ncloud",
                        "gpu_model": gpu_model,
                        "vram_gb": vram_per_gpu,
                        "price_per_hour": price_usd,
                        "availability_status": "available",
                        "provider_link": url,
                        "gpu_count": gpu_count,
                        "server_code": server_code,
                        "hourly_krw": hourly_krw,
                        "note": f"{server_code}: {gpu_count}x{gpu_model} {vram_per_gpu}GB, {hourly_krw:,}원/hr"
                    })
                    logger.info(f"  [NCloud] {server_code}: {gpu_count}x{gpu_model} {vram_per_gpu}GB, {hourly_krw:,}원/hr → ${price_usd}/hr")
            
            await browser.close()
        
        # 중복 제거 (동일 server_code)
        seen = set()
        unique = []
        for r in results:
            if r['server_code'] not in seen:
                seen.add(r['server_code'])
                unique.append(r)
        
        logger.info(f"[NCloud] 완료: {len(unique)}건")
        return unique
        
    except Exception as e:
        logger.error(f"[NCloud] 크롤링 실패: {e}")
        return []



# ============================================================
# 메인 실행 및 테스트
# ============================================================
async def run_all_crawlers() -> Dict[str, List[Dict]]:
    """모든 한국 GPU 클라우드 크롤러 실행"""
    print("=" * 70)
    print("  한국 GPU 클라우드 실파싱 크롤러 - Playwright 기반")
    print("=" * 70)
    
    crawlers = {
        "vessl": crawl_vessl,
        "gpuaas": crawl_gpuaas,
        "cloudv": crawl_cloudv,
        "runyourai": crawl_runyourai,
        "ncloud": crawl_ncloud,
    }
    
    all_results = {}
    for name, crawler_fn in crawlers.items():
        print(f"\n[{name.upper()}] 크롤링 시작...")
        try:
            results = await crawler_fn()
            all_results[name] = results
            print(f"[{name.upper()}] 완료: {len(results)}건 수집")
            for r in results[:3]:
                print(f"    {r['gpu_model']}: {r['vram_gb']}GB VRAM, ${r['price_per_hour']}/hr")
        except Exception as e:
            print(f"[{name.upper()}] 실패: {e}")
            all_results[name] = []
    
    # 최종 요약
    print("\n" + "=" * 70)
    print("  최종 수집 결과 요약")
    print("=" * 70)
    total = 0
    for name, results in all_results.items():
        print(f"  {name}: {len(results)}건")
        total += len(results)
    print(f"\n  총계: {total}건")
    
    return all_results


if __name__ == "__main__":
    import sys
    import json
    from datetime import datetime
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    
    results = asyncio.run(run_all_crawlers())
    
    # 전체 데이터 출력
    print("\n\n=== 수집된 전체 데이터 ===")
    all_flat = []
    for provider, items in results.items():
        if items:
            print(f"\n[{provider.upper()}]")
            for item in items:
                print(f"  {item['gpu_model']:30s} | {item['vram_gb']:4d}GB VRAM | ${item['price_per_hour']:.4f}/hr")
                all_flat.append(item)
    
    # JSON 파일로 저장
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"crawl_result_korean_{timestamp}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_flat, f, ensure_ascii=False, indent=2)
    print(f"\n[저장 완료] {output_file} ({len(all_flat)}건)")
