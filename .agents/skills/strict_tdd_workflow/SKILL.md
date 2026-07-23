---
name: strict_tdd_workflow
description: Enforce strict Test-Driven Development (TDD) workflow (1 Dev -> 1 Test -> 1 Verify -> 1 Deploy) for all implementations and maintain clean directory structures.
---

# Strict TDD Workflow Rule (엄근진 TDD 및 디렉터리 관리 규칙)

**[절대 원칙]**
우리의 개발 프로세스는 반드시 **1개발 -> 1테스트케이스 -> 1검증 -> 1배포** 순서를 따라야 합니다. 어떠한 경우에도 테스트 코드를 누락해서는 안 됩니다.

## 1. Directory Structure (디렉터리 구조 엄수)
- 백엔드 테스트 코드는 반드시 `tests/` 디렉터리 내부의 적절한 도메인 폴더에 작성합니다.
  - 예: `apps/services/market/crawler.py` 구현 시 -> `tests/services/market/test_crawler.py` 생성
- 프론트엔드 테스트 코드는 `apps/web/__tests__/` 또는 해당 컴포넌트와 동일한 위치에 `.test.tsx` 확장자로 작성합니다.

## 2. 1개발 (Development)
- 기능(모듈, 컴포넌트, 엔드포인트 등)을 구현할 때는 항상 단일 책임 원칙(SRP)과 느슨한 결합(Loose Coupling)을 고려하여 작성합니다.
- 하드코딩을 지양하고 환경변수와 설정 파일(`config.py`, `.env`)을 적극 활용합니다.

## 3. 1테스트케이스 (Test Case Creation)
- **개발이 완료된 즉시(또는 개발과 동시에) 단위 테스트(Unit Test)를 작성합니다.**
- 파이썬 백엔드의 경우 `pytest`를 사용하며, 외부 API 호출(Naver, Coupang 등)이 포함된 경우 반드시 `pytest-mock` 또는 `responses`를 활용하여 모킹(Mocking)합니다.
- 비동기 로직이 있는 경우 `pytest-asyncio`를 사용합니다.

## 4. 1검증 (Verification)
- 코드를 커밋하기 전, 혹은 사용자에게 완료를 보고하기 전에 반드시 해당 테스트 코드를 터미널에서 구동하여 `PASS`를 확인해야 합니다.
- 명령어 예시: `pytest tests/services/market/test_crawler.py -v`
- 전체 테스트 커버리지 및 성공 여부를 확인합니다.

## 5. 1배포 (Deployment / Git Push)
- 테스트가 모두 통과(PASS)한 것이 확인된 경우에만 Git 커밋(`commit`)과 푸시(`push`)를 진행합니다.
- Git 메시지는 작업 내역과 테스트 포함 여부를 명시적으로 작성합니다. (예: `feat: Add Coupang crawler with unit tests`)

이 규칙은 모든 에이전트 작업에 **가장 최우선(Strict)**으로 적용됩니다.
