"""
tests/integration/conftest.py
통합 테스트 공통 설정: FastAPICache InMemoryBackend 초기화
"""
import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


@pytest.fixture(scope="session", autouse=True)
def init_fastapi_cache():
    """세션 레벨 FastAPICache 초기화"""
    FastAPICache.init(InMemoryBackend(), prefix="integration-test-cache")
    yield
