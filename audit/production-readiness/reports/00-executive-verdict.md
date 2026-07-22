# AMEVA InfraIndex Platform — Production Readiness Forensic Audit
# Executive Verdict

**Audit Date:** 2026-07-22T17:20 ~ 17:40 KST  
**Auditor:** Independent Production Readiness Audit Team (Principal SWE Architect, Backend/Frontend/DB/SRE/DevOps/Security/Data Quality/Distributed Systems/Test Reliability/FinOps/License Compliance/DR Auditors)  
**Audit Scope:** Full static code analysis + partial dynamic verification  
**HEAD Commit:** `858d3cc65ac28ef3a7f5036c354730a041c07f3a`  
**Branch:** `main`  
**Git Remote:** `https://github.com/uno-km/infraindex-platform.git`

---

# ⛔ 최종 판정

## **NO-GO**

---

# 한 줄 결론

> **"이 시스템을 오늘 production에 올리면 인증 없는 관리자 API, 하드코딩 Mock 가격 데이터, 미구현 DB 저장 파이프라인, 빈 Outbox 소비자, 완전히 연결되지 않은 수집→저장→표시 파이프라인으로 인해 사용자에게 가짜 데이터를 제공하고 관리자 기능이 무방비 상태로 노출된다."**

---

# 신뢰도

**Medium**

### 신뢰도 제한 이유:
- Docker Compose 실제 빌드 실행 불가 (시간 제약)
- PostgreSQL 격리 환경 migration round-trip 미실행
- 실제 외부 API (Vast.ai, RunPod) 연동 라이브 테스트 미실행
- pytest 실제 실행 불가 (DB 의존성)
- Terraform terraform validate 미실행 (terraform 미설치)
- 정적 코드 분석으로 대부분 판정

---

# 검증 범위

| 범주 | 상태 |
|---|---|
| 전체 저장소 파일 정적 분석 | ✅ 완료 |
| 모든 Python 소스 코드 리딩 | ✅ 완료 |
| 모든 API 엔드포인트 구현 확인 | ✅ 완료 |
| DB Migration 파일 전수조사 | ✅ 완료 |
| ORM ↔ Migration 일치성 확인 | ✅ 완료 (정적) |
| Git 추적 파일 및 Secret 감사 | ✅ 완료 |
| Docker Compose 설정 검토 | ✅ 완료 (정적) |
| Terraform 설정 검토 | ✅ 완료 (정적) |
| Celery 설정 검토 | ✅ 완료 |
| Provider 크롤러 구현 확인 | ✅ 완료 |
| Render Blueprint 검토 | ✅ 완료 |
| 테스트 파일 품질 분석 | ✅ 완료 |
| Docker 실제 빌드 실행 | ❌ NOT TESTED |
| pytest 실제 실행 | ❌ NOT TESTED (DB 의존성) |
| Alembic migration 실행 | ❌ NOT TESTED (PostgreSQL 미기동) |
| 실제 API HTTP 테스트 | ❌ NOT TESTED |
| Celery worker 실제 기동 | ❌ NOT TESTED |
| Terraform validate | ❌ NOT TESTED (미설치) |
| 실제 크롤러 라이브 호출 | ❌ NOT TESTED |
| 백업/복구 실제 테스트 | ❌ NOT TESTED |

---

# 🔴 Critical Findings (즉시 배포 불가)

| ID | 제목 | 심각도 |
|---|---|---|
| AMEVA-CRIT-001 | 관리자 API 완전 무인증 | CRITICAL |
| AMEVA-CRIT-002 | 차트 API 전체가 하드코딩 Mock 데이터 반환 | CRITICAL |
| AMEVA-CRIT-003 | PostgreSQL Storage 완전 미구현 - 수집 데이터가 DB에 저장 안 됨 | CRITICAL |
| AMEVA-CRIT-004 | AWS 크롤러가 하드코딩된 가짜 데이터 반환 | CRITICAL |
| AMEVA-CRIT-005 | Outbox Publisher/Consumer 완전 부재 - Outbox 이벤트 소비 불가 | CRITICAL |
| AMEVA-CRIT-006 | Celery Beat 등록 Task명 불일치 - Beat 작동 시 task 미발견 | CRITICAL |
| AMEVA-CRIT-007 | History API가 항상 빈 배열 반환 | CRITICAL |
| AMEVA-CRIT-008 | Chat API가 Mock Scaffold 반환 | CRITICAL |
| AMEVA-CRIT-009 | Wildcard CORS (`["*"]`) 기본값 - production 위험 | CRITICAL |
| AMEVA-CRIT-010 | 하드코딩 DB 기본 비밀번호 `password` | CRITICAL |

---

# 🟠 High Findings

| ID | 제목 | 심각도 |
|---|---|---|
| AMEVA-HIGH-001 | QuarantineService가 크롤러 파이프라인과 연결되지 않음 | HIGH |
| AMEVA-HIGH-002 | IdempotencyKey가 실제 task에서 사용되지 않음 | HIGH |
| AMEVA-HIGH-003 | CircuitBreaker가 크롤러에 연결되지 않음 | HIGH |
| AMEVA-HIGH-004 | Celery Beat 스케줄의 task 이름이 실제 task 이름과 불일치 | HIGH |
| AMEVA-HIGH-005 | Rate Limiter가 인메모리 - 분산 환경에서 무효 | HIGH |
| AMEVA-HIGH-006 | Health Check가 `CELERY_BROKER_URL` 참조하나 config에 정의 안 됨 | HIGH |
| AMEVA-HIGH-007 | Terraform: RDS public 접근성, 서브넷 없음, 삭제 보호 없음 | HIGH |
| AMEVA-HIGH-008 | SSE가 DB 폴링 방식이나 연결당 세션 누수 가능 | HIGH |
| AMEVA-HIGH-009 | Reports Excel/Word API에 실제 DB 데이터 없음 (Mock) | HIGH |
| AMEVA-HIGH-010 | USE_REAL_DB=False가 기본값 - production 전환 누락 위험 | HIGH |
| AMEVA-HIGH-011 | Render Blueprint에 Celery Beat 스케줄러 서비스 없음 | HIGH |
| AMEVA-HIGH-012 | Render Blueprint가 free plan - production에 부적합 | HIGH |
| AMEVA-HIGH-013 | Search API: quarantine된 가격도 검색 결과에 포함 | HIGH |
| AMEVA-HIGH-014 | backup_db.sh에 S3 업로드가 주석 처리됨 - offsite 백업 없음 | HIGH |
| AMEVA-HIGH-015 | 가격에 Float 사용 (price_history 테이블) - 부동소수점 오차 | HIGH |

---

# 핵심 기능 판정표

| 기능 | 상태 | 근거 |
|---|---|---|
| **데이터 수집** | ⚠️ PARTIAL | Vast.ai: 실제 API 호출 코드 존재. RunPod: GraphQL 호출 코드 존재. **AWS: 하드코딩된 Mock 데이터** |
| **스케줄러** | ❌ FAIL | Celery Beat에 등록된 `orchestrator.run_all_collections`가 실제 task명 `orchestrator.tick`과 불일치. Beat 실행 시 `NotRegistered` 오류 발생 |
| **DB 저장** | ❌ FAIL | `PostgresStorage.save()`가 `logger.info()` 한 줄뿐, 실제 INSERT 없음. 기본값 `USE_REAL_DB=False` |
| **품질 격리** | ❌ DISCONNECTED | `QuarantineService` 존재하나 파이프라인에서 호출되지 않음 |
| **검색** | ⚠️ PARTIAL | 코드 구조 양호하나 DB에 데이터가 없으면 항상 빈 결과 |
| **차트** | ❌ FAIL | `chart.py`가 하드코딩된 3개 데이터포인트 반환. DB 미연결 |
| **Outbox** | ⚠️ PARTIAL | `PostgresOutboxEventBus` 클래스 존재하나 PriceObservation 저장 시 실제로 호출되지 않음. Publisher 완전 부재 |
| **SSE** | ⚠️ PARTIAL | Outbox DB 폴링 방식으로 구현됨. Outbox에 데이터 없으면 이벤트 없음 |
| **관리자** | ❌ CRITICAL FAIL | 인증 0개. 누구나 `/api/v1/admin/quarantine` 접근 가능 |
| **배포 (Docker)** | ⚠️ NOT TESTED | Compose 설정 문법상 타당하나 실제 빌드/기동 미확인 |
| **배포 (Render)** | ⚠️ PARTIAL | Blueprint 존재하나 Celery Beat 누락, free plan, start command 미지정 |
| **복구** | ❌ PARTIAL | backup_db.sh 존재하나 S3 업로드 주석처리, 복구 테스트 없음 |

---

# 보고서 정확성 검증

| 주장 | 상태 | 실제 증거 |
|---|---|---|
| "PostgreSQL 저장 완료" | ❌ 과장 | `PostgresStorage.save()` = `logger.info()` 한 줄뿐 |
| "Outbox Dual-Write 완전 방지" | ❌ 거짓 | PriceObservation 저장 코드에서 OutboxEvent 동시 기록 없음 |
| "5분마다 병렬 크롤러 실행" | ❌ 불완전 | Beat task명 불일치로 실제 실행 안 됨 |
| "AWS 크롤러가 실제 데이터 수집" | ❌ 거짓 | 하드코딩 Mock `{"sku": "P4d.24xlarge"}` 반환 |
| "DataQualityIssue 격리 정책 완성" | ❌ 과장 | QuarantineService가 파이프라인에 연결되지 않음 |
| "차트가 실제 DB 이력 표시" | ❌ 거짓 | 3개 하드코딩 데이터포인트 반환 |
| "IdempotencyKey가 중복 실행 방지" | ❌ GHOST | 코드 존재하나 orchestrator에서 호출 없음 |
| "초고속 트렌드 분석 복합 인덱스" | ⚠️ 과장 | 인덱스는 존재하나 조회 코드가 미구현 |
| "관리자 인증 완비" | ❌ 거짓 | 인증 코드 0줄 |
| "Alembic migration 4개 완비" | ✅ 정확 | 마이그레이션 파일 4개 실제 존재 확인 |
| "13~15개 테이블" | ✅ 정확 | Migration에서 실제 15개 테이블 구조 확인 |

---

# 지금 배포하면 발생할 수 있는 일

```
1. USE_REAL_DB=False (기본값)이므로 모든 수집 데이터가 로컬 JSON 파일에 저장됨.
   - Docker 재시작 시 데이터 소실
   - DB 기반 검색은 항상 빈 결과 반환

2. Celery Beat 실행 시 task 이름 불일치로 'orchestrator.run_all_collections' NotRegistered 오류.
   - 크롤링이 전혀 실행되지 않음
   - 사용자에게 stalte 또는 빈 데이터 표시

3. 차트 페이지: 항상 "2026-07-20~22 Vast.ai H100 $1.85~2.10" 동일한 하드코딩 데이터 표시.
   - 날짜가 흘러도 차트는 항상 동일.
   - 사용자는 가짜 데이터를 실시간 가격으로 오인.

4. GET /api/v1/admin/quarantine 및 POST /api/v1/admin/quarantine/{id}/approve 인증 없음.
   - 인터넷 어디서나 누구든 quarantine 목록 조회 및 release 가능.
   
5. AWS 크롤러: 실제 AWS API 없이 항상 P4d.24xlarge 1개, $32.77 반환.

6. Reports Excel/Word: 항상 동일한 Vast.ai H100 Mock 데이터 다운로드.
   - 사용자가 다운받는 Excel에 실제 가격 없음.

7. 수집 장애 시 알림 없음 (ENABLE_ALERTS=False 기본값).
   - 운영팀이 장애를 인지하지 못함.
```

---

# 배포 전에 반드시 고쳐야 할 항목 (우선순위 순)

### P0 — 즉시 (배포 완전 차단)
1. **관리자 API 인증 구현** (`admin.py` - API Key 또는 JWT 최소한 필요)
2. **Wildcard CORS를 production 도메인으로 제한** (`config.py` L9)
3. **하드코딩 DB 비밀번호 제거** (환경변수로 완전 전환)
4. **차트 API Mock 제거 및 실제 DB 연결 구현** (`chart.py`)
5. **Celery Beat task명 수정** (`celery_app.py` L27: `orchestrator.run_all_collections` → `orchestrator.tick`)

### P1 — production 전 필수
6. **PostgresStorage.save() 실제 구현** (현재 logger.info() 뿐)
7. **QuarantineService를 파이프라인에 연결** (orchestrator에 호출 코드 추가)
8. **IdempotencyKey를 orchestrator에서 실제 사용**
9. **Outbox를 PriceObservation 저장 시 동일 트랜잭션으로 기록**
10. **Outbox Publisher 구현** (현재 소비자 완전 부재)
11. **AWS 크롤러 실제 구현** (boto3 또는 AWS Pricing API)
12. **History API 구현** (현재 항상 `{"history": []}`)
13. **Rate Limiter를 Redis 백엔드로 전환** (분산 환경)
14. **Health Check의 CELERY_BROKER_URL 참조 오류 수정**
15. **USE_REAL_DB=True를 production 기본값으로**

### P2 — 안정화
16. Search API quarantine 필터링 추가
17. Circuit Breaker를 실제 HTTP 호출에 연결
18. CollectionRun을 orchestrator에서 실제 생성
19. Render Blueprint에 Celery Beat 서비스 추가
20. Terraform RDS 삭제 보호, 서브넷, 암호화 추가
21. S3 백업 활성화

---

# 제한적 배포 가능 범위

**현 상태에서 안전하게 배포 가능한 범위는 없음.**

단, 다음 P0 항목 수정 후 제한적 내부 데모(internal demo only) 가능:
- 관리자 인증 추가
- CORS 도메인 제한
- USE_REAL_DB=False 모드로 JSON 파일 기반 읽기 전용 대시보드

단, 이 경우에도 사용자에게 "데모 데이터"임을 명시해야 함.
