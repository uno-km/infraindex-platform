# Remediation Plan — P0~P3 우선순위 수정 계획

감사일: 2026-07-22  
판정: **NO-GO**

---

## P0 — 즉시 배포 차단 (차단 해제 전 필수)

---

### P0-001: 관리자 API 인증 구현
**관련 Finding:** AMEVA-CRIT-001  
**파일:** `apps/api/api/v1/endpoints/admin.py`

**제안 변경:**
```python
# 최소한 API Key 방어막 추가
from fastapi import Header, HTTPException
import os

ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "")

async def verify_admin(x_api_key: str = Header(...)):
    if not ADMIN_API_KEY or x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

# 모든 admin 엔드포인트에 Depends(verify_admin) 추가
@router.get("/quarantine", dependencies=[Depends(verify_admin)])
```

**완료 기준:** 인증 없이 /api/v1/admin/** 호출 시 403 반환  
**예상 난이도:** Easy (2-4시간)  
**배포 차단:** YES

---

### P0-002: Wildcard CORS 제한
**관련 Finding:** AMEVA-CRIT-009  
**파일:** `apps/api/core/config.py`

**제안 변경:**
```python
# Before
BACKEND_CORS_ORIGINS: list[str] = ["*"]

# After
BACKEND_CORS_ORIGINS: list[str] = []  # 반드시 env에서 주입
```

**환경변수 필수화:** `BACKEND_CORS_ORIGINS='["https://your-domain.com"]'`  
**완료 기준:** 빈 origin으로 시작, 반드시 env에서 허용 도메인 명시  
**예상 난이도:** Easy (30분)

---

### P0-003: 하드코딩 기본 비밀번호 제거
**관련 Finding:** AMEVA-CRIT-010  
**파일:** `apps/api/core/config.py`, `infrastructure/docker/docker-compose.yml`

**제안 변경:**
```python
# config.py
POSTGRES_PASSWORD: str  # 기본값 없음 → env 미설정 시 시작 실패
```

**완료 기준:** 비밀번호 없이 시작 시 ValidationError 발생  
**예상 난이도:** Easy (1시간)

---

### P0-004: Celery Beat Task명 수정
**관련 Finding:** AMEVA-CRIT-006  
**파일:** `apps/worker/celery_app.py`

**제안 변경:**
```python
# Before
"task": "orchestrator.run_all_collections",

# After  
"task": "orchestrator.tick",
```

**완료 기준:** Celery Beat 실행 후 `task_success` 이벤트 확인  
**예상 난이도:** Easy (30분) — 단, 실제 동작 검증 필요

---

### P0-005: 차트 API Mock 제거 및 실제 DB 연결
**관련 Finding:** AMEVA-CRIT-002  
**파일:** `apps/api/api/v1/endpoints/chart.py`

**제안 변경:**
```python
# PriceHistory 테이블 쿼리
from apps.api.models.history import PriceHistory
from sqlalchemy import select, and_

stmt = (
    select(PriceHistory)
    .where(PriceHistory.provider_id == provider_id)
    .where(PriceHistory.gpu_model.ilike(f"%{gpu_model_id}%"))
    .order_by(PriceHistory.timestamp.asc())
)
```

**완료 기준:** DB에 실제 데이터 삽입 후 차트 API가 동적 응답 반환  
**예상 난이도:** Medium (2-5일) — PriceHistory writer 구현 선행 필요

---

## P1 — Production 전 필수

---

### P1-001: PostgresStorage.save() 실제 구현
**관련 Finding:** AMEVA-CRIT-003  
**파일:** `apps/worker/core/storage.py`

```python
class PostgresStorage(BaseStorage):
    async def save(self, provider_slug: str, data: List[Dict[str, Any]]) -> None:
        from apps.api.core.database import AsyncSessionLocal
        from apps.api.models.history import PriceHistory
        from datetime import datetime, timezone
        
        async with AsyncSessionLocal() as session:
            async with session.begin():
                for item in data:
                    record = PriceHistory(
                        provider_id=provider_slug,
                        gpu_model=item.get("gpu_model", "Unknown"),
                        vram_gb=item.get("vram_gb", 0.0),
                        price_per_hour=item.get("price_per_hour", 0.0),
                        availability_status=item.get("availability_status", "unknown"),
                        timestamp=datetime.now(timezone.utc)
                    )
                    session.add(record)
```

**완료 기준:** 수집 후 price_history 테이블에 실제 row 확인  
**예상 난이도:** Medium (2-3일)

---

### P1-002: QuarantineService 파이프라인 연결 + 키 불일치 수정
**관련 Finding:** AMEVA-HIGH-001, AMEVA-MED-002  
**파일:** `apps/worker/tasks/orchestrator.py`, `apps/worker/core/quarantine.py`

```python
# orchestrator.py에 추가
from apps.worker.core.quarantine import QuarantineService

async def execute_extraction(provider_slug: str):
    ...
    normalized_data = await crawler.execute_pipeline()
    
    # 품질 검사
    quality_result = QuarantineService.inspect(normalized_data)
    passed_data = quality_result["passed"]
    quarantined = quality_result["quarantined"]
    
    if quarantined:
        logger.warning(f"[{provider_slug}] {len(quarantined)} items quarantined")
        # TODO: CollectionRun과 연결하여 DataQualityIssue 저장
    
    await storage.save(provider_slug, passed_data)  # passed만 저장

# quarantine.py 키 수정
if item.get("price_per_hour", 0) < 0:  # hourly_price → price_per_hour
```

**예상 난이도:** Medium (2-3일)

---

### P1-003: IdempotencyKey orchestrator 연결
**관련 Finding:** AMEVA-HIGH-002  
**파일:** `apps/worker/tasks/orchestrator.py`

```python
from apps.worker.core.idempotency import acquire_lock
from datetime import date

async def execute_extraction(provider_slug: str):
    key = f"{provider_slug}:{date.today().isoformat()}:{int(time.time() // 300)}"
    # 5분 버킷으로 중복 방지
    ...
```

**예상 난이도:** Medium (1-2일)

---

### P1-004: CollectionRun orchestrator 연결
**관련 Finding:** AMEVA-HIGH-013

```python
# orchestrator에서 CollectionRun 생성
async with AsyncSessionLocal() as db:
    run = CollectionRun(
        provider_id=...,
        started_at=datetime.now(timezone.utc),
        status="running"
    )
    db.add(run)
    await db.commit()
    try:
        ...
        run.status = "success"
        run.items_collected = len(passed_data)
    except Exception as e:
        run.status = "failed"
    finally:
        run.completed_at = datetime.now(timezone.utc)
        await db.commit()
```

**예상 난이도:** Medium (2-3일)

---

### P1-005: Health Check CELERY_BROKER_URL 수정
**관련 Finding:** AMEVA-HIGH-005  
**파일:** `apps/api/api/v1/endpoints/health.py:37`

```python
# Before
redis_client = redis.from_url(settings.CELERY_BROKER_URL)

# After
redis_client = redis.from_url(settings.REDIS_URL)
```

**예상 난이도:** Easy (15분)

---

### P1-006: Rate Limiter Redis 백엔드 전환
**관련 Finding:** AMEVA-HIGH-004  
**파일:** `apps/api/core/limiter.py`

```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.backends.redis import RedisBackend
from apps.api.core.config import settings

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.REDIS_URL
)
```

**예상 난이도:** Easy (2-4시간)

---

### P1-007: USE_REAL_DB=True를 production 기본값으로
**관련 Finding:** AMEVA-HIGH-011  

**Render Blueprint 수정:**
```yaml
- key: USE_REAL_DB
  value: "True"
```

**Docker Compose 수정 필요.**  
**예상 난이도:** Easy (1시간)

---

### P1-008: Render Blueprint에 Celery Beat 서비스 추가
**관련 Finding:** AMEVA-HIGH-007  

```yaml
- type: worker
  name: infraindex-celery-beat
  env: docker
  dockerfilePath: apps/worker/Dockerfile
  startCommand: celery -A apps.worker.celery_app beat --loglevel=info
  plan: starter
```

**예상 난이도:** Easy (1-2시간)

---

## P2 — 안정화 (30일 내)

- Search API quarantine 필터링 추가
- Terraform RDS: 삭제 보호, 서브넷 그룹, 암호화, Multi-AZ 추가
- Circuit Breaker 실제 HTTP 클라이언트에 연결 (분산 Redis 백엔드 필요)
- S3 백업 활성화 (`backup_db.sh` 주석 해제 + AWS 자격증명 주입)
- AWS 크롤러 실제 구현 (boto3 pricing API 또는 공개 JSON 인덱스)
- History API 실제 구현
- Reports API DB 연결
- SSE DB 세션 누수 수정 (connection당 session 분리)
- Vast.ai 라이선스 법무 검토

---

## P3 — 장기 개선 (90일 내)

- PriceObservation 저장 시 OutboxEvent 동일 트랜잭션 기록
- Outbox Publisher worker 구현
- 검색 퍼지/관련도 점수 개선
- Chat/NLP 기능 실제 구현
- 통합/E2E 테스트 슈트 구축 (pytest-asyncio + testcontainers)
- Prometheus alerting 규칙 및 Grafana 대시보드 추가
- TimescaleDB 도입 검토 (hypertable for price_history)
- BaseProviderAdapter dead code 제거

---

## 수정 완료 기준 (최소 GO 요건)

1. GET /api/v1/admin/* → 인증 없이 403 반환
2. CORS origin = production 도메인만
3. Celery Beat 실행 → orchestrator.tick 성공적으로 dispatch
4. Vast.ai, RunPod 수집 → price_history 테이블에 실제 row 생성
5. 차트 API → DB의 실제 데이터 반환
6. History API → 실제 이력 반환
7. Health Check → DB 및 Redis 연결 성공 확인
8. Docker Compose up → 전체 스택 기동 성공
9. Alembic upgrade head → 빈 DB에서 성공
10. 격리된 환경에서 E2E-01 시나리오 통과
