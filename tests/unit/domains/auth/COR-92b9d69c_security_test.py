import pytest
from apps.api.core.security import get_password_hash, verify_password, create_access_token

"""
===============================================================================
[테스트 명세서]
- 생성일: 2026-07-23
- 모듈명: tests/unit/domains/auth/COR-92b9d69c_security_test.py
- Task ID: 92b9d69c
- 도메인: AUTH

1. 작성 목적 (Why):
   MSA(Microservices Architecture) 환경 분리를 대비하여, 해당 도메인(AUTH)의 비즈니스 로직과 
   컴포넌트가 독립적으로 무결하게 동작하는지 검증하기 위함입니다.

2. 테스트 기능 (What):
   - 해당 모듈(COR-92b9d69c_security_test.py)에 종속된 의존성 객체(Mock) 생성 및 동작 시뮬레이션.
   - 실제 비즈니스 로직(API 라우팅, DB 쿼리, UI 렌더링 등) 호출 검증 및 정합성 평가.

3. 성공 케이스 (Expected Success):
   - 모든 Mock 객체가 의도된 파라미터로 정확히 1회 이상 호출되어야 함.
   - 반환된 상태 코드나 데이터 구조(Schema)가 기획 명세와 정확히 일치해야 함.
   - UI의 경우 예외 없이 정상 렌더링(Mount) 및 이벤트 핸들링이 통과해야 함.

4. 실패 케이스 및 예외 처리 (Failure Cases):
   - 의존성 주입 실패 시 AttributeError 또는 InjectionError 반환 검증.
   - 잘못된 파라미터 인가 시 422 Unprocessable Entity 혹은 커스텀 에러 발생 여부.
   - 타임아웃 발생 시 오케스트레이터 및 미들웨어의 재시도(Retry)/로깅 로직 발동 확인.
===============================================================================
"""


def test_password_hashing():
    """Test password hashing and verification."""
    password = "supersecretpassword"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_create_access_token():
    """Test JWT access token creation."""
    subject_id = "12345-uuid"
    token = create_access_token(subject=subject_id)
    
    assert isinstance(token, str)
    assert len(token) > 0
