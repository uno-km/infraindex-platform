# PostgreSQL 데이터베이스 스키마 명세서 & 테이블 정의서 보고서

본 보고서는 `InfraIndex Platform`의 수집 데이터(JSON)를 **PostgreSQL RDBMS로 안정적으로 이관 및 퍼시스턴스 보장**하기 위한 **데이터베이스 아키텍처, 테이블 상세 정의서, 인덱싱 최적화 전략**을 기술합니다.

---

## 1. 아키텍처 개요 (Architecture Overview)

- **RDBMS 선택:** PostgreSQL 16 (PostGIS / JSONB 지원)
- **비동기 드라이버:** AsyncPG (`postgresql+asyncpg://`)
- **트랜잭션 패턴:** Outbox Pattern (시세 INSERT와 Pub/Sub 이벤트 발행의 원자성 보장)
- **시계열 관리:** 주 단위 / 월 단위 파티셔닝 준비 및 인덱싱

---

## 2. 테이블 정의서 (Table Specifications)

### 2.1. `price_history` (GPU 클라우드 인스턴스 시세 이력)
* **목적:** 전 세계 10개 프로바이더의 시간당 GPU 임대 시세를 저장하는 핵심 시계열 테이블.

| 컬럼명 (Column) | 데이터 타입 (Type) | 제약 조건 (Constraint) | 설명 (Description) |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY`, Default `gen_random_uuid()` | 고유 식별자 |
| `provider_id` | `VARCHAR(50)` | `NOT NULL` | 제공사 식별자 (`vast-ai`, `aws`, `runpod` 등) |
| `gpu_model` | `VARCHAR(100)` | `NOT NULL` | GPU 모델명 (`A100`, `H100`, `RTX 4090` 등) |
| `vram_gb` | `NUMERIC(6,2)` | `NOT NULL` | VRAM 용량 (GB 단위) |
| `price_per_hour` | `NUMERIC(10,4)` | `NOT NULL`, `CHECK (price_per_hour > 0)` | GPU 1개당 1시간 임대 단가 ($) |
| `availability_status`| `VARCHAR(50)` | `NOT NULL`, Default `'available'` | 재고 상태 (`available`, `unassigned`) |
| `instance_type` | `VARCHAR(100)` | `NULLABLE` | 프로바이더별 인스턴스 규격명 (`p4d.24xlarge`) |
| `sys_ram_gb` | `INTEGER` | `NULLABLE` | 시스템 RAM (GB) |
| `tdp_w` | `INTEGER` | `NULLABLE` | 소비전력 (TDP Watt) |
| `provider_link` | `TEXT` | `NULLABLE` | 할당/구매 웹 링크 |
| `timestamp` | `TIMESTAMPTZ` | `NOT NULL`, Default `NOW()` | 수집 시각 (UTC) |

* **인덱싱 전략 (Indexing):**
  - `idx_price_history_model_ts`: `(gpu_model, timestamp DESC)` ➔ 특정 GPU의 30일 시세 차트 조회 최적화
  - `idx_price_history_provider_ts`: `(provider_id, timestamp DESC)` ➔ 프로바이더별 최신가 조회
  - `idx_price_history_ts`: `(timestamp DESC)` ➔ 시계열 데이터 범위 검색

---

### 2.2. `retail_price_history` (리테일 RAM, CPU, B2B 하드웨어 시세)
* **목적:** 이커머스(다나와, 아마존 등) 및 B2B 유통망의 하드웨어 부품 가격 저장.

| 컬럼명 (Column) | 데이터 타입 (Type) | 제약 조건 (Constraint) | 설명 (Description) |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY` | 고유 식별자 |
| `hardware_type` | `VARCHAR(30)` | `NOT NULL` | 유형 (`ram`, `cpu`, `gpu`, `enterprise_gpu`) |
| `model_name` | `VARCHAR(150)` | `NOT NULL` | 하드웨어 모델명 (`DDR5 32GB`, `RTX 4090`) |
| `manufacturer` | `VARCHAR(50)` | `NULLABLE` | 제조사 (`samsung`, `nvidia`, `amd`) |
| `platform` | `VARCHAR(50)` | `NOT NULL` | 판매 플랫폼 (`danawa`, `coupang`, `amazon`) |
| `price` | `NUMERIC(12,2)` | `NOT NULL` | 판매 가격 |
| `currency` | `VARCHAR(10)` | `NOT NULL`, Default `'KRW'` | 통화 (`KRW`, `USD`) |
| `capacity_gb` | `NUMERIC(6,2)` | `NULLABLE` | 용량 (GB) |
| `product_url` | `TEXT` | `NULLABLE` | 상품 구매 URL |
| `is_official` | `BOOLEAN` | `DEFAULT FALSE` | 공식 총판 여부 |
| `timestamp` | `TIMESTAMPTZ` | `NOT NULL`, Default `NOW()` | 수집 시각 |

* **인덱싱 전략 (Indexing):**
  - `idx_retail_type_model_ts`: `(hardware_type, model_name, timestamp DESC)` ➔ 리테일 OHLC 차트 조회 최적화

---

### 2.3. `financial_market_history` (반도체 주식 & DRAM 선물 지수)
* **목적:** NVDA, SK하이닉스, 삼성전자 주가 및 DRAM Exchange 선물 시세 저장.

| 컬럼명 (Column) | 데이터 타입 (Type) | 제약 조건 (Constraint) | 설명 (Description) |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY` | 고유 식별자 |
| `symbol` | `VARCHAR(20)` | `NOT NULL` | 티커 Symbol (`NVDA`, `000660.KS`, `DXR`) |
| `asset_type` | `VARCHAR(30)` | `NOT NULL` | 구분 (`stock`, `dram_futures`) |
| `open` | `NUMERIC(12,4)` | `NOT NULL` | 시가 |
| `high` | `NUMERIC(12,4)` | `NOT NULL` | 고가 |
| `low` | `NUMERIC(12,4)` | `NOT NULL` | 저가 |
| `close` | `NUMERIC(12,4)` | `NOT NULL` | 종가 |
| `volume` | `BIGINT` | `NULLABLE` | 거래량 |
| `currency` | `VARCHAR(10)` | `NOT NULL`, Default `'USD'` | 통화 |
| `timestamp` | `TIMESTAMPTZ` | `NOT NULL`, Default `NOW()` | 기준 시각 |

* **인덱싱 전략 (Indexing):**
  - `idx_financial_symbol_ts`: `(symbol, timestamp DESC)` ➔ 마켓 인사이트 주식 상관관계 비교 최적화

---

### 2.4. `news_articles` (글로벌 반도체 & AI 뉴스)
* **목적:** 3-Tier 수집된 글로벌 반도체 뉴스 저장 및 중복 방지.

| 컬럼명 (Column) | 데이터 타입 (Type) | 제약 조건 (Constraint) | 설명 (Description) |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY` | 고유 식별자 |
| `title` | `VARCHAR(300)` | `NOT NULL` | 기사 제목 |
| `url` | `TEXT` | `UNIQUE`, `NOT NULL` | 기사 원문 URL (중복 수집 방지) |
| `source` | `VARCHAR(50)` | `NOT NULL` | 언론사/출처 (`Reuters`, `TechCrunch`) |
| `published_at` | `TIMESTAMPTZ` | `NOT NULL` | 기사 발행 일시 |
| `summary` | `TEXT` | `NULLABLE` | AI/자동 요약문 |
| `keywords` | `VARCHAR(200)` | `NULLABLE` | 태그/키워드 (`HBM3e`, `NVIDIA`) |
| `collection_tier` | `VARCHAR(20)` | `NOT NULL`, Default `'tier1'` | 수집 티어 (`tier1_rss`, `tier2_api`, `tier3`) |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL`, Default `NOW()` | DB 저장 시각 |

* **인덱싱 전략 (Indexing):**
  - `uq_news_url`: `UNIQUE (url)` ➔ 동일 기사 중복 INSERT 방지
  - `idx_news_published`: `(published_at DESC)` ➔ 최신 뉴스 50건 순차 출력

---

### 2.5. `outbox_events` (트랜잭션 보장 Outbox 이벤트)
* **목적:** DB INSERT와 Redis Pub/Sub 이벤트 발행 간의 원자성(Atomicity) 보장.

| 컬럼명 (Column) | 데이터 타입 (Type) | 제약 조건 (Constraint) | 설명 (Description) |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY` | 고유 식별자 |
| `topic` | `VARCHAR(100)` | `NOT NULL` | 메시지 토픽 (`price_updates`) |
| `event_type` | `VARCHAR(100)` | `NOT NULL` | 이벤트 유형 (`price.collected`) |
| `payload` | `JSONB` | `NOT NULL` | 이벤트 본문 데이터 (JSON) |
| `status` | `VARCHAR(20)` | `NOT NULL`, Default `'pending'` | 처리 상태 (`pending`, `published`, `failed`) |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL`, Default `NOW()` | 생성 시각 |

* **인덱싱 전략 (Indexing):**
  - `idx_outbox_pending`: `(created_at ASC) WHERE status = 'pending'` ➔ 미처리 이벤트 고속 스캔 Partial Index

---

## 3. 설정 파일 중심 구성 방안 (No Source Code Changes)

소스코드를 단 한 줄도 건드리지 않고, **설정 파일만으로 로컬 DB 환경을 완벽 제어**하는 가이드입니다:

1. **`infrastructure/docker/docker-compose.yml` (컨테이너 설정):**
   - PostgreSQL 16 버전을 포트 `5432`로 바인딩하고 프로젝트 루트 `.docker_data` 폴더에 물리 볼륨을 연결하여 데이터를 격리 보장.
2. **`.env` (환경 설정):**
   - `USE_REAL_DB=True`로 전환 시 파이썬 코드가 자동으로 PostgreSQL 인프라로 스위칭됩니다.
3. **`alembic.ini` (DB 마이그레이션 설정):**
   - 소스 수정 없이 `alembic -c alembic.ini upgrade head` 명령어 실행만으로 상기 9개 테이블과 인덱스가 100% 자동 생성됩니다.
