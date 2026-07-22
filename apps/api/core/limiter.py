"""
P1-004: Rate Limiter — Redis 백엔드로 전환.

기존 인메모리 slowapi.Limiter는 분산 환경(멀티 pod)에서
각 pod가 독립적인 카운터를 유지하므로 실질적 제한이 무의미.

slowapi는 redis 백엔드를 위해 limits 라이브러리의 RedisStorage를 사용.
REDIS_URL 미설정 시 graceful fallback으로 메모리 모드 유지.
"""
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from apps.api.core.config import settings

logger = logging.getLogger(__name__)


def _build_limiter() -> Limiter:
    """
    REDIS_URL이 설정되어 있으면 Redis 백엔드 Limiter를 반환.
    설정이 없거나 연결 실패 시 in-memory fallback.
    """
    redis_url = getattr(settings, "REDIS_URL", None)
    if redis_url:
        try:
            # slowapi uses the 'limits' library which accepts the storage_uri kwarg
            limiter = Limiter(
                key_func=get_remote_address,
                storage_uri=redis_url,
            )
            logger.info(f"[RateLimiter] Redis 백엔드 초기화: {redis_url.split('@')[-1]}")
            return limiter
        except Exception as e:
            logger.warning(
                f"[RateLimiter] Redis 백엔드 초기화 실패 ({e}). "
                "in-memory fallback 사용 (단일 인스턴스에서만 정확함)."
            )

    logger.warning("[RateLimiter] REDIS_URL 미설정 — in-memory fallback 사용.")
    return Limiter(key_func=get_remote_address)


limiter = _build_limiter()
