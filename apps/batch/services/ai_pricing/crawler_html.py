import asyncio
import httpx
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from shared.db.session import AsyncSessionLocal
from shared.models.ai_pricing import AIModelMaster, AIModelPriceHistory
from shared.core.exceptions.decorators import notify_on_error
from sqlalchemy.future import select

logger = logging.getLogger(__name__)

# 타겟 사이트 매핑
TARGET_URLS = {
    "anthropic": "https://www.anthropic.com/pricing",
    "openai": "https://openai.com/pricing",
    "baidu": "https://cloud.baidu.com/doc/WENXINWORKSHOP/s/hlrnm09lu" # ERNIE Bot
}

def extract_price_heuristic(text: str) -> float | None:
    """
    휴리스틱: 텍스트에서 달러 기호($)나 가격 패턴을 찾아 플로트로 반환.
    """
    # 아주 단순화된 휴리스틱
    import re
    match = re.search(r'\$([0-9]+\.?[0-9]*)', text)
    if match:
        val = float(match.group(1))
        # 가격 정합성 체크 (1M 당 가격이 0~200달러 사이가 아니면 이상치로 판단)
        if 0 < val < 200:
            return val
    return None

@notify_on_error(severity="CRITICAL", source="crawler_html_fallback")
async def crawl_html_pricing():
    """
    공식 홈페이지에서 가격표를 파싱합니다. API에 없는 모델들을 대상으로 합니다.
    DOM이나 CSS가 변경되어 휴리스틱에 실패하면 즉시 예외(Exception)를 발생시켜 텔레그램 경고를 날립니다.
    """
    logger.info("Starting HTML Fallback Pricing Crawler...")

    async with httpx.AsyncClient() as client:
        # Example 1: Anthropic 파싱 (의도적으로 CSS 셀렉터를 엄격하게 혹은 틀리게 작성해 에러 감지 테스트 가능)
        try:
            res = await client.get(TARGET_URLS["anthropic"], timeout=10.0)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')

            # 실제로는 복잡한 테이블 파싱이 필요. 여기서는 시뮬레이션 로직
            # 홈페이지 구조가 자주 바뀌므로 이 부분은 잘 터짐 -> 텔레그램 발송의 주요 원인.
            price_element = soup.select_one(".pricing-table .claude-3-5-sonnet-input")
            
            if not price_element:
                raise ValueError("Anthropic Pricing table CSS selector ('.pricing-table .claude-3-5-sonnet-input') not found. DOM might have changed.")

            input_price_1m = extract_price_heuristic(price_element.text)
            if input_price_1m is None:
                raise ValueError(f"Failed to extract valid price from Anthropic page. Text: {price_element.text[:50]}")

            # DB 저장 로직 (생략 - OpenRouter 크롤러와 동일한 upsert)
            logger.info(f"Successfully scraped Anthropic: Input ${input_price_1m}")

        except httpx.HTTPStatusError as e:
            # 403 Forbidden 등
            raise RuntimeError(f"HTTP Error during HTML scraping: {e}")

    logger.info("HTML Fallback Pricing Crawler Finished.")

def run_html_crawler():
    asyncio.run(crawl_html_pricing())

