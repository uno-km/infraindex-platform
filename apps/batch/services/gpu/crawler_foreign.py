from typing import Any, Dict, List
from apps.batch.worker.providers.common.base import BaseProviderCrawler

class XesktopCrawler(BaseProviderCrawler):
    """
    Xesktop GPU 렌탈 사이트 크롤러.
    실파싱이 구현될 때까지 빈 결과를 반환하여 목업 데이터 유입을 방지.
    TODO: Playwright 기반 실파싱 구현 (https://xesktop.com/price/ 참고)
    """
    @property
    def provider_slug(self) -> str:
        return "xesktop"

    async def fetch_raw_data(self) -> Any:
        self.logger.warning("[xesktop] 실파싱 미구현 - 빈 결과 반환 (목업 데이터 사용 중단)")
        return []

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        return raw_data if isinstance(raw_data, list) else []

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return parsed_data
