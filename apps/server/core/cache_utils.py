import functools
from fastapi import Response
from cachetools import TTLCache, cached

# 1. CDN & Browser Cache Decorator (Dependency Injection)
def get_cache_control(max_age: int = 60, s_maxage: int = 3600, stale_while_revalidate: int = 600):
    """
    FastAPI 의존성 주입용 함수. 
    Vercel/Cloudflare 등 CDN과 브라우저 캐싱을 위한 Cache-Control 헤더를 설정합니다.
    """
    def dependency(response: Response):
        response.headers["Cache-Control"] = f"public, max-age={max_age}, s-maxage={s_maxage}, stale-while-revalidate={stale_while_revalidate}"
    return dependency

# 2. Server In-Memory Cache (Local Cache)
# 자주 변경되지 않는 공통 데이터(예: 메타데이터, 카테고리)를 로컬 서버 메모리에 캐싱
local_memory_cache = TTLCache(maxsize=1000, ttl=300) # 최대 1000개 아이템, 5분 TTL

def in_memory_cache(ttl=300):
    """
    서버 로컬 메모리에 함수의 반환값을 캐싱합니다. Redis까지 가지 않아도 될 때 사용합니다.
    """
    def decorator(func):
        cache = TTLCache(maxsize=1000, ttl=ttl)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return cached(cache)(func)(*args, **kwargs)
        return wrapper
    return decorator
