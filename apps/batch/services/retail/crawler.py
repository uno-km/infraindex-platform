from typing import Any, Dict, List
import asyncio
import logging

logger = logging.getLogger(__name__)

class RetailUniversalCrawler:
    """
    리테일 가격 크롤러 통합 인터페이스.
    Naver Shopping API + Coupang Affiliate API 실크롤링으로 데이터를 수집합니다.
    목업 데이터를 완전히 제거하고 실 API를 사용합니다.
    """
    name = "retail_universal"

    async def sync_to_db(self, db) -> Dict[str, Any]:
        """
        Naver + Coupang 크롤러를 순차적으로 실행하여 실제 가격 데이터를 DB에 적재합니다.
        """
        from apps.batch.services.market.crawler_retail import RetailCrawler
        from apps.batch.services.market.crawler_coupang import CoupangCrawler

        results = {
            "status": "success",
            "naver": {},
            "coupang": {},
        }

        # 1. Naver Shopping 크롤링
        logger.info("[RetailUniversal] Naver Shopping 크롤러 시작...")
        try:
            naver_crawler = RetailCrawler()
            naver_result = await naver_crawler.sync_to_db(db)
            results["naver"] = naver_result
            logger.info(f"[RetailUniversal] Naver 완료: {naver_result}")
        except Exception as e:
            logger.error(f"[RetailUniversal] Naver 크롤러 실패: {e}")
            results["naver"] = {"status": "error", "message": str(e)}
            results["status"] = "partial"

        # 2. Coupang 크롤링 (API 호출 분산을 위해 1초 대기 후 실행)
        await asyncio.sleep(1.0)
        logger.info("[RetailUniversal] Coupang 크롤러 시작...")
        try:
            coupang_crawler = CoupangCrawler()
            coupang_result = await coupang_crawler.sync_to_db(db)
            results["coupang"] = coupang_result
            logger.info(f"[RetailUniversal] Coupang 완료: {coupang_result}")
        except Exception as e:
            logger.error(f"[RetailUniversal] Coupang 크롤러 실패: {e}")
            results["coupang"] = {"status": "error", "message": str(e)}
            results["status"] = "partial"

        return results
