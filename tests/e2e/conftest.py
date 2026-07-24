"""
tests/e2e/conftest.py
E2E 테스트 공통 설정: FastAPICache InMemoryBackend 초기화 + get_db override
"""
import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


@pytest.fixture(scope="session", autouse=True)
def init_fastapi_cache():
    """세션 레벨 FastAPICache 초기화 (Redis 없이 InMemory 사용)"""
    FastAPICache.init(InMemoryBackend(), prefix="e2e-test-cache")
    yield
