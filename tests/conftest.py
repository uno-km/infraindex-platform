"""
tests/conftest.py
전체 테스트 공통 설정
- TRUSTED_HOSTS에 testserver 추가 (TestClient/httpx 기본 Host 헤더)
- FastAPICache InMemoryBackend 초기화
"""
import pytest
import os


def pytest_configure(config):
    """
    pytest 설정 시점에 TRUSTED_HOSTS 환경변수를 설정하여
    TestClient(base_url=testserver) 요청이 TrustedHostMiddleware를 통과하도록 한다.
    """
    # JSON list 형식으로 설정 (pydantic-settings가 파싱)
    os.environ.setdefault(
        "TRUSTED_HOSTS",
        '["localhost", "127.0.0.1", "testserver", "test", "*"]'
    )
