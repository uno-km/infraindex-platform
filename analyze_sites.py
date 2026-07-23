"""
Step 1: 각 사이트 HTML 구조 분석 스크립트
Playwright로 각 사이트에 접속해서 HTML을 덤프하고
가격 관련 텍스트 패턴을 추출해 파싱 전략 수립
"""
import asyncio
import re
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SITES = {
    "cloudv": "https://cloudv.kr/server/gpu.html",
    "vessl": "https://vessl.ai/ko/pricing",
    "gpuaas": "https://gpuaas.kr/",
    "runyourai": "https://console.runyour.ai/gpu-cloud",
    "ktcloud": "https://cloud.kt.com/",
    "ncloud": "https://www.ncloud.com/product/compute/gpuServer",
}

PRICE_PATTERNS = [
    r'(\d+(?:\.\d+)?)\s*(?:원|KRW|₩)',           # Korean won prices
    r'\$\s*(\d+(?:,\d{3})*(?:\.\d+)?)',            # USD dollar sign
    r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:USD|/hr|/h|시간)',  # USD or per hour
    r'(\d{1,3}(?:,\d{3})+)\s*원',                  # e.g. 2,500원
    r'(\d+(?:\.\d+)?)\s*(?:GB|VRAM|G)',            # VRAM sizes
]

GPU_PATTERNS = [
    r'H100', r'A100', r'A10', r'L40', r'V100', r'RTX\s*\d{4}',
    r'T4', r'MI300', r'B200', r'RTX\s*3090', r'RTX\s*4090',
]

async def analyze_site(name: str, url: str):
    print(f"\n{'='*60}")
    print(f"[{name.upper()}] {url}")
    print('='*60)
    
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            print(f"  Navigating...")
            await page.goto(url, wait_until="networkidle", timeout=45000)
            
            # Extra wait for dynamic content
            await page.wait_for_timeout(3000)
            
            # Try to find and print page title
            title = await page.title()
            print(f"  Page title: {title}")
            
            # Get full rendered HTML
            html = await page.content()
            print(f"  HTML length: {len(html)} chars")
            
            # Check for AJAX requests by monitoring network
            # Also get text content (no HTML tags) for easy pattern matching
            text = await page.evaluate("() => document.body.innerText")
            
            # Find GPU models mentioned
            print(f"\n  --- GPU Models Found ---")
            for pattern in GPU_PATTERNS:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    unique = list(set(matches))
                    print(f"    {pattern}: {unique[:5]}")
            
            # Find price patterns
            print(f"\n  --- Price Patterns Found ---")
            for pattern in PRICE_PATTERNS:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    unique = list(set(matches[:10]))
                    print(f"    {pattern}: {unique[:5]}")
            
            # Find table elements
            tables = await page.query_selector_all('table')
            print(f"\n  --- Tables: {len(tables)} found ---")
            for i, table in enumerate(tables[:3]):
                table_text = await table.inner_text()
                print(f"    Table {i+1} preview: {table_text[:200]!r}")
            
            # Find elements with price-like classes
            price_selectors = [
                '[class*="price"]', '[class*="cost"]', '[class*="fee"]',
                '[class*="plan"]', '[class*="pricing"]', '[class*="rate"]',
                '[class*="tier"]', '[class*="요금"]', '[class*="price"]'
            ]
            print(f"\n  --- Price-class Elements ---")
            for sel in price_selectors:
                els = await page.query_selector_all(sel)
                if els:
                    first_text = await els[0].inner_text()
                    print(f"    {sel}: {len(els)} elements, first: {first_text[:100]!r}")
            
            # Dump first 3000 chars of body text for analysis
            print(f"\n  --- Body Text (first 2000 chars) ---")
            print(text[:2000])
            
            # Save full HTML for manual inspection
            with open(f"html_dump_{name}.html", "w", encoding="utf-8") as f:
                f.write(html)
            print(f"\n  [Saved to html_dump_{name}.html]")
            
            await browser.close()
            return True
            
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {e}")
        return False


async def main():
    print("=== 사이트별 HTML 구조 분석 시작 ===")
    print("각 사이트에 Playwright로 접속해서 가격 데이터 구조 파악")
    
    for name, url in SITES.items():
        success = await analyze_site(name, url)
        print(f"\n  -> {name}: {'SUCCESS' if success else 'FAILED'}")

if __name__ == "__main__":
    asyncio.run(main())
