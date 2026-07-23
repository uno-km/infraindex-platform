# 엔터프라이즈 전용 표준 약어(Abbreviation) 준수 지침 (Skill Rule)

## 📌 핵심 원칙 (Core Principles)

1. **영문 원문 풀네임 금지 ➔ 2~5글자 숏 약어(Abbreviation) 100% 통일**
   - 영문 풀네임(`semiconductor`, `microprocessor`, `observability`, `autoscaling`, `transaction`, `budget`)을 그대로 쓰지 않고, 사전에 정의된 **2~5글자 숏 약어**만을 사용한다.
   - **주요 표준 약어 정제 목록:**
     - `semiconductor` ➔ **`semi`**
     - `microprocessor` ➔ **`mpu`**
     - `microcontroller` ➔ **`mcu`**
     - `observability` ➔ **`obs`**
     - `instrumentation` ➔ **`inst`**
     - `autoscaling` ➔ **`asc`**
     - `securitization` ➔ **`secu`**
     - `collateralization` ➔ **`clt`**
     - `inspection` ➔ **`insp`**
     - `budget` ➔ **`bdgt`**
     - `transaction` ➔ **`tx`**
     - `provider` ➔ **`pvd`**
     - `request` ➔ **`req`**
     - `response` ➔ **`res`**
     - `document` ➔ **`doc`**
     - `identifier` ➔ **`id`**
     - `benchmark` ➔ **`bnch`**
     - `user` ➔ **`user`**

2. **표준 약어 조합 규칙**
   - 개발자 및 AI는 사전에 있는 숏 약어를 `_`로 조합하여 컬럼명 및 변수명을 작성한다.
   - **조합 예시:** `req_doc_id`, `semi_mpu_cd`, `bdgt_prc_amt`, `tx_cnt`

3. **테이블 접두사 규격 (`tbl_`)**
   - 모든 DB 물리 테이블명은 접두사 **`tbl_`**로 시작한다 (예: `tbl_gpu_prc_hist`, `tbl_semi_mpu_stat`, `tbl_news_arti`).
