# 엔터프라이즈 정밀 순수 원자(Atomic) 약어 사전 & 명명 규칙 정의서

본 문서는 `InfraIndex Platform`의 모든 데이터베이스 테이블, 컬럼명, DTO, 백엔드/프론트엔드 코드 변수명의 **순수 원자적(Atomic) 숏 약어 239개 사전과 조합 규칙**을 정의합니다.

---

## 📌 핵심 설계 원칙 (User Feedback Core Rule)

1. **합성어 완전 금지 (Zero Compound Words):**
   * 사전에는 `sys_orgn`이나 `sysorgn` 같은 **합성어를 절대 수록하지 않습니다.**
   * 오직 더 이상 쪼갤 수 없는 **원자적(Atomic) 숏 약어 단어인 `sys` (시스템)와 `orgn` (원천/소체)만 독립된 항목으로 사전에 수록**합니다.

2. **실제 코딩 및 DB 명명 시 결합 규칙 (`_` 연결):**
   * 코딩이나 테이블/컬럼 설계 시 사전에 수록된 원자 약어들을 **언더스코어(`_`)로 결합**하여 사용합니다.
   * **조합 예시:**
     * 시스템 원천 ➔ **`sys_orgn`** (`sys` + `orgn`)
     * 요청 문서 식별자 ➔ **`req_doc_id`** (`req` + `doc` + `id`)
     * 반도체 MPU 코드 ➔ **`semi_mpu_cd`** (`semi` + `mpu` + `cd`)
     * 예산 금전 금액 ➔ **`bdgt_prc_amt`** (`bdgt` + `prc` + `amt`)
     * 트랜잭션 건수 ➔ **`tx_cnt`** (`tx` + `cnt`)

---

## 📁 파일 위치

1. **마이크로소프트 엑셀 호환 순수 원자 약어 CSV 사전 (239개 수록):** [`docs/data_dictionary.csv`](file:///c:/Users/GAME/Desktop/uno-km/dev/AMEVA-Memory-Price-Check/docs/data_dictionary.csv)
2. **개발자용 마크다운 정의서:** [`docs/DATA_DICTIONARY.md`](file:///c:/Users/GAME/Desktop/uno-km/dev/AMEVA-Memory-Price-Check/docs/DATA_DICTIONARY.md)
3. **스킬즈 수록 지침:** [`.skills/enterprise_naming_convention.md`](file:///c:/Users/GAME/Desktop/uno-km/dev/AMEVA-Memory-Price-Check/.skills/enterprise_naming_convention.md)
4. **글로벌 프로젝트 규칙:** [`.cursorrules`](file:///c:/Users/GAME/Desktop/uno-km/dev/AMEVA-Memory-Price-Check/.cursorrules#L18-L23)

---

## 1. 대표 순수 원자 약어 샘플 (전체 239개는 CSV 참조)

| 표준원자약어 (Atomic Abbr) | 한글의미 | 영어풀네임 | 설명 | 비고 |
|---|---|---|---|---|
| **`sys`** | **시스템** | **System** | 전체 소프트웨어 시스템 | System |
| **`orgn`** | **원천소체** | **Origin** | 데이터 발생 소스 오리진 | System |
| **`semi`** | **반도체** | **Semiconductor** | 반도체 부품 소자 | Hardware |
| **`mpu`** | **마이크로프로세서** | **Microprocessor** | 연산 제어 프로세서 MPU | Hardware |
| **`mcu`** | **마이크로컨트롤러** | **Microcontroller** | 임베디드 제어 칩셋 MCU | Hardware |
| **`obs`** | **가관측성** | **Observability** | 통합 관제 가관측성 | DevOps |
| **`inst`** | **계측코드** | **Instrumentation** | 모니터링 코드 주입 | DevOps |
| **`asc`** | **자동증설** | **Auto Scaling** | 부하 감지 자동 확장 | DevOps |
| **`bdgt`** | **예산** | **Budget** | 인프라 운영 예산 | Finance |
| **`tx`** | **트랜잭션** | **Transaction** | 금융 및 시스템 거래 | Finance |
| **`pvd`** | **제공사** | **Provider** | 클라우드 인프라 제공업체 | Hardware |
| **`req`** | **요청** | **Request** | 서비스 및 데이터 요청 | Communication |
| **`res`** | **응답** | **Response** | 서비스 응답 데이터 | Communication |
| **`doc`** | **문서** | **Document** | 전자 문서 자원 | Communication |
| **`id`** | **식별자** | **Identifier** | 고유 식별 ID | Database |
| **`user`** | **유저** | **User** | 서비스 사용자 계정 | User |
| **`bnch`** | **벤치마크** | **Benchmark** | 성능 평가 지표 | Metric |
| **`tbl`** | **테이블** | **Table** | DB 물리 테이블 접두사 | Database |
