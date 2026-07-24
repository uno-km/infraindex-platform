from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

# 단일 GPU 시간당 최대 합리적 가격 ($1,000/hr 초과는 이상 데이터)
MAX_PRICE_PER_HOUR = 1000.0
# 음수 가격 하한
MIN_PRICE_PER_HOUR = 0.0


class QuarantineService:
    """
    P1-001: 파이프라인 연결 완료.
    수집 데이터의 가격 이상치·필수 필드 누락을 감지하여 격리.

    수정사항:
    - 'hourly_price' → 'price_per_hour' 키 불일치 수정 (크롤러 실제 필드명)
    - 'gpu_model'/'gpu_name' 둘 다 허용
    - 필수 필드 누락 검사 추가
    """

    @staticmethod
    def inspect(raw_data: List[Dict[str, Any]]) -> dict:
        """
        정규화 데이터에서 품질 이슈를 검사한다.
        Returns:
            {
                "passed": [정상 데이터 리스트],
                "quarantined": [{"data": ..., "issues": [...]} 리스트]
            }
        """
        passed = []
        quarantined = []

        for item in raw_data:
            issues = []

            # --- 가격 추출 (크롤러별 키 이름 통일) ---
            # providers/ 계열: price_per_hour
            # adapters/ 계열: hourly_price
            price = item.get("price_per_hour") or item.get("hourly_price")

            # Rule 1: 가격 필드 누락
            if price is None:
                issues.append("missing_price_field")
            else:
                price = float(price)
                # Rule 2: 음수 가격
                if price < MIN_PRICE_PER_HOUR:
                    issues.append("negative_price")
                # Rule 3: 비이성적 고가 ($1,000/hr 초과)
                if price > MAX_PRICE_PER_HOUR:
                    issues.append("extreme_variance")

            # Rule 4: GPU 모델명 누락
            gpu_name = item.get("gpu_model") or item.get("gpu_name")
            if not gpu_name:
                issues.append("missing_gpu_name")

            if issues:
                quarantined.append({"data": item, "issues": issues})
                logger.warning(
                    f"[Quarantine] Item blocked due to {issues} | "
                    f"gpu={gpu_name!r} price={price!r}"
                )
            else:
                passed.append(item)

        return {"passed": passed, "quarantined": quarantined}
