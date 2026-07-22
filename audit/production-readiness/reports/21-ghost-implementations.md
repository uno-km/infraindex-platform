# Ghost Implementations — 연결되지 않은 코드 목록

감사일: 2026-07-22  
조사방법: 전체 저장소 정적 분석 + 호출 그래프 추적

---

## 정의
**Ghost Implementation**: 코드는 존재하지만 실제 실행 경로에서 호출되지 않거나,
존재한다고 주장되는 기능이 실제로는 완전히 미구현된 항목.

---

## GHOST-001: PostgresStorage.save() — 빈 구현체

| 항목 | 내용 |
|---|---|
| 파일 | `apps/worker/core/storage.py` L28-32 |
| 주장 | "PostgreSQL에 실제 데이터 저장" |
| 실제 코드 | `logger.info(f"[{provider_slug}] Saved {len(data)} records to PostgreSQL Database")` |
| 실제 동작 | 로그만 출력, INSERT 없음 |
| 영향 | USE_REAL_DB=True로 설정해도 DB에 아무 것도 저장되지 않음 |
| 심각도 | CRITICAL |

```python
class PostgresStorage(BaseStorage):
    async def save(self, provider_slug: str, data: List[Dict[str, Any]]) -> None:
        # Scaffold for Postgres. Real implementation would use SQLAlchemy AsyncSession
        # and insert into PriceHistory table.
        logger.info(f"[{provider_slug}] Saved {len(data)} records to PostgreSQL Database")
        # ← 실제 DB INSERT 코드 완전 부재
```

---

## GHOST-002: QuarantineService — 호출되지 않는 격리 서비스

| 항목 | 내용 |
|---|---|
| 파일 | `apps/worker/core/quarantine.py` |
| 주장 | "이상 가격 자동 격리 (quarantine severity)" |
| 실제 상태 | 클래스와 규칙은 구현됨. 하지만 orchestrator.py에서 호출 없음 |
| 호출 위치 | 없음 — 파이프라인 어디서도 import되지 않음 |
| 심각도 | HIGH — 음수가격, 극단가격이 격리 없이 저장 가능 |

```python
# orchestrator.py에서 QuarantineService 미사용
# quarantine.py 내 규칙: item.get("hourly_price") 키를 검사하지만
# 실제 크롤러가 "price_per_hour" 키를 사용하여 키 불일치도 존재
```

---

## GHOST-003: IdempotencyKey — 존재하나 호출 없음

| 항목 | 내용 |
|---|---|
| 파일 | `apps/worker/core/idempotency.py` |
| 주장 | "동일 스케줄 중복 실행 방지" |
| 실제 상태 | `acquire_lock()` 함수 존재. orchestrator.py에서 import 없음 |
| 증거 | orchestrator.py grep 결과: `idempotency` 관련 import/호출 없음 |
| 심각도 | HIGH |

---

## GHOST-004: CircuitBreaker — 인스턴스화되지 않음

| 항목 | 내용 |
|---|---|
| 파일 | `apps/worker/core/circuit_breaker.py` |
| 주장 | 서킷 브레이커 패턴으로 공급자 장애 격리 |
| 실제 상태 | 클래스 구현됨. 어떤 크롤러에서도 사용 없음 |
| 추가 문제 | 인메모리 상태 → 분산 환경에서 worker 재시작 시 초기화 |
| 심각도 | MEDIUM |

---

## GHOST-005: Outbox Publisher — 완전 부재

| 항목 | 내용 |
|---|---|
| 관련 파일 | `apps/api/core/events/bus.py`, `apps/api/models/outbox.py` |
| 주장 | "Transactional Outbox Pattern으로 이벤트 스트리밍" |
| 생산자 상태 | `PostgresOutboxEventBus.publish()` 클래스 존재하나 PriceObservation 저장 경로에서 호출 없음 |
| 소비자 상태 | **완전 부재** — outbox_events를 읽어서 외부 브로커로 발행하는 worker 없음 |
| SSE와의 관계 | stream.py가 outbox_events를 DB 폴링하지만 Outbox에 데이터가 채워지지 않음 |
| 심각도 | CRITICAL |

---

## GHOST-006: AWS 크롤러 — 하드코딩 Mock

| 항목 | 내용 |
|---|---|
| 파일 | `apps/worker/providers/aws.py` L9-12 |
| 주장 | "AWS EC2/Spot API 크롤러" |
| 실제 코드 | 하드코딩된 `{"sku": "P4d.24xlarge", "gpu": "A100"}` 반환 |
| 실제 동작 | 항상 `price_per_hour: 32.77` 반환 |
| 심각도 | CRITICAL |

```python
async def fetch_raw_data(self) -> Any:
    # AWS Pricing API is usually fetched via Boto3 or public JSON index
    # Scaffold for Phase 15
    return {"products": [{"sku": "P4d.24xlarge", "attributes": {"memory": "1152 GiB", "gpu": "A100"}}]}
```

---

## GHOST-007: Chart API — 하드코딩 Mock 3개 데이터포인트

| 항목 | 내용 |
|---|---|
| 파일 | `apps/api/api/v1/endpoints/chart.py` L33-43 |
| 주장 | "실제 DB PriceHistory 기반 차트" |
| 실제 동작 | 어떤 입력에도 동일한 3개 데이터포인트 반환 |
| 심각도 | CRITICAL |

---

## GHOST-008: History API — 항상 빈 배열

| 항목 | 내용 |
|---|---|
| 파일 | `apps/api/api/v1/endpoints/history.py` L18-19 |
| 주장 | "가격 이력 조회 API" |
| 실제 코드 | `# TODO: Implement history logic` → `return {"offering_id": offering_id, "history": []}` |
| 심각도 | CRITICAL |

---

## GHOST-009: Chat API — Mock Scaffold

| 항목 | 내용 |
|---|---|
| 파일 | `apps/api/api/v1/endpoints/chat.py` L27-33 |
| 주장 | "NLP Query Engine" |
| 실제 동작 | 항상 "NLP feature is currently in scaffolding phase" 반환 |
| 심각도 | HIGH |

---

## GHOST-010: Admin 관리자 인증 — 완전 부재

| 항목 | 내용 |
|---|---|
| 파일 | `apps/api/api/v1/endpoints/admin.py` |
| 주장 | "관리자 전용 API (Admin only)" |
| 실제 인증 | 없음. `Depends(get_db)` 뿐 |
| 취약점 | 인터넷 어디서나 누구든 quarantine 목록 조회 및 release 가능 |
| 심각도 | CRITICAL |

---

## GHOST-011: Celery Beat Task명 불일치

| 항목 | 내용 |
|---|---|
| 파일 | `apps/worker/celery_app.py` L27 |
| Beat 등록 task | `orchestrator.run_all_collections` |
| 실제 task명 | `orchestrator.tick` (orchestrator.py L47) |
| 결과 | Celery Beat 실행 시 `NotRegistered: orchestrator.run_all_collections` 오류 → 크롤링 전혀 실행 안 됨 |
| 심각도 | CRITICAL |

---

## GHOST-012: PriceHistory 기록 주체 없음

| 항목 | 내용 |
|---|---|
| 관련 | `apps/api/models/history.py` — PriceHistory 모델 |
| 주장 | "가격 변경 이력 누적" |
| 실제 상태 | 테이블 모델과 migration은 존재. 하지만 어떤 코드도 이 테이블에 INSERT하지 않음 |
| 심각도 | HIGH |

---

## GHOST-013: CollectionRun 생성 주체 없음

| 항목 | 내용 |
|---|---|
| 관련 | `apps/api/models/quality.py` — CollectionRun 모델 |
| 주장 | "크롤러 수집 실행 로그" |
| 실제 상태 | orchestrator.py에서 CollectionRun INSERT 없음 |
| 심각도 | HIGH |

---

## GHOST-014: ScheduleConfig — 실제 스케줄러에 미사용

| 항목 | 내용 |
|---|---|
| 관련 | `apps/api/models/scheduler.py` — ScheduleConfig 모델 |
| 주장 | "동적 스케줄 설정" |
| 실제 상태 | 모델과 테이블은 존재. celery_app.py는 고정 crontab 사용, ScheduleConfig 테이블 조회 없음 |
| 심각도 | MEDIUM |

---

## GHOST-015: Reports API — Mock 데이터

| 항목 | 내용 |
|---|---|
| 파일 | `apps/api/api/v1/endpoints/reports.py` L37-44 |
| 주장 | "실제 DB 데이터 기반 Excel/Word 내보내기" |
| 실제 코드 | `mock_data = [["2026-07-20", "Vast.ai", gpu_model_id, 1.85, 1.95, 2.10], ...]` |
| 심각도 | HIGH |

---

## GHOST-016: BaseAdapter — 사용되지 않는 추상 클래스

| 항목 | 내용 |
|---|---|
| 파일 | `apps/worker/core/base_adapter.py` |
| 실제 상태 | `BaseProviderCrawler` (providers/common/base.py)와 `BaseProviderAdapter` (core/base_adapter.py) 두 개 존재. 크롤러는 base_adapter.py를 import하지 않음 |
| 심각도 | LOW (dead code) |

---

## 요약 통계

| 심각도 | Ghost 수 |
|---|---|
| CRITICAL | 7개 |
| HIGH | 6개 |
| MEDIUM | 2개 |
| LOW | 1개 |
| **합계** | **16개** |
