# Scaffold & Mock 전수 조사 — TODO/Mock/Scaffold 코드 54개 발견

감사일: 2026-07-22  
탐색 명령: `Select-String -Pattern "TODO|mock_data|scaffold|Scaffold|return \[\]|return {}" -Recurse *.py, *.ts, *.tsx`  
발견 건수: **54개 (중복 포함)**  
고유 파일 수: **12개 파일에 걸쳐 분포**

---

## 중요도별 분류

### 🔴 CRITICAL — 운영 데이터에 직접 영향

| 파일 | 행 | 내용 | 심각도 |
|---|---|---|---|
| `storage.py` | 30 | `# Scaffold for Postgres. Real implementation would use SQLAlchemy` | CRITICAL |
| `aws.py` | 11 | `# Scaffold for Phase 15` + 하드코딩 반환 | CRITICAL |
| `chart.py` | 29,32 | `Phase 9 Scaffold - Returns mocked downsampled data` | CRITICAL |
| `reports.py` | 37-43 | `# Mock data insertion (In prod, fetch from DB)` + `mock_data = [...]` | CRITICAL |
| `history.py` | 18 | `# TODO: Implement history logic` | CRITICAL |
| `data_service.py` | 15-16 | `# TODO: Implement Postgres reading logic` → `return []` | CRITICAL |

### 🟠 HIGH — 기능 미구현

| 파일 | 행 | 내용 | 심각도 |
|---|---|---|---|
| `chat.py` | 25,27,31 | `Mock Scaffold for Phase 8` + TODO + mock response | HIGH |
| `admin.py` | 39 | `# TODO: Fetch issue, extract payload, push to PriceObservation` | HIGH |
| `ai_service.py` | 7,38 | `Scaffold: If no API key, use mock response` | HIGH |
| `memory_crawler.py` | 10-16 | `# Scaffold for Phase 14` + 하드코딩 메모리 가격 | HIGH |
| `news_crawler.py` | 13-19 | `# Scaffold for Phase 14` + 하드코딩 뉴스 3개 | HIGH |
| `power_crawler.py` | 10-16 | `# Scaffold for Phase 14` + 하드코딩 전력비용 | HIGH |
| `alerts.py` | 7 | `# Fallback webhook URL for scaffold testing` | MEDIUM |
| `stream.py` | 32 | `# Mark processed (Simplified for scaffold)` | MEDIUM |

### ⚪ INFO — 정상적인 추상 클래스 pass (허용)

| 파일 | 내용 |
|---|---|
| `bus.py` L10 | abstract method `pass` — 정상 |
| `base.py` L8 | `DeclarativeBase` 정상 |
| `base_adapter.py` L6,11,16,21,26 | abstract method `pass` — 정상 |
| `idempotency.py` L8 | `LockAcquisitionError(Exception): pass` — 정상 |
| `storage.py` L15 | abstract method `pass` — 정상 |
| `base.py` L20,25,30,38 | abstract method `pass` — 정상 |

---

## 아키텍처적 결론

프로젝트의 실제 구현 완성도를 Phase 기준으로 정리:

```
Phase 1-8:  모노레포 구조, DB 모델, API 라우터 구조 — ✅ 존재
Phase 9:    차트 API — ⚠️ Scaffold (하드코딩 데이터)
Phase 14:   메모리·뉴스·전력 크롤러 — ❌ 전부 Mock
Phase 15:   AWS 크롤러 — ❌ Mock
Phase ?:    PostgresStorage — ❌ logger.info() 뿐
Phase ?:    History API — ❌ TODO
Phase ?:    Chat/NLP — ❌ Scaffold
Phase ?:    Admin 관리 기능 — ❌ TODO
```

**실제 완성된 기능:**
- Vast.ai API HTTP 호출 코드 ✅ (실제 동작 미확인)
- RunPod GraphQL 호출 코드 ✅ (인증 없이, 실제 동작 미확인)  
- DB 스키마 및 Migration ✅
- 검색 엔진 구조 (코드) ✅ — 단, DB 데이터 없으면 항상 빈 결과

**프로젝트는 Phase 8~9 구조 설계 단계이며, Phase 14~15 이상의 핵심 기능이 Scaffold/Mock 상태다.**

---

## RunPod 아키텍처 중복 문제 (추가 발견)

**두 가지 RunPod 구현체가 동시에 존재:**

1. `apps/worker/providers/runpod.py` — `BaseProviderCrawler` 기반 (orchestrator에서 호출)
2. `apps/worker/adapters/runpod/client.py` — `BaseProviderAdapter` 기반 (어디서도 호출 안 됨)

- `RunpodAdapter`는 CircuitBreaker를 실제로 연결하는 더 완성된 구현체
- 하지만 orchestrator에서 import되는 것은 `RunpodCrawler` (providers/runpod.py)
- CircuitBreaker가 있는 adapter는 **Dead Code**

이는 리팩토링 중에 두 구조가 충돌한 것으로 보임.
