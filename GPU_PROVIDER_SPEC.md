# 글로벌 클라우드 GPU 수집 파이프라인 명세서

| 프로바이더 (Provider) | 수집 대상 URL (Source URL) | 수집 방식 (Method) | 수집 건수 | 최근 가져온 대표 수집 실측 시세 (샘플) |
|---|---|---|---|---|
| **VAST-AI** | https://console.vast.ai/api/v0/bundles/ | REST API (GET) | 64건 | RTX 5090 ($0.058/h), A100 80GB ($1.350/h), H100 ($2.490/h) |
| **RUNPOD** | https://api.runpod.io/graphql | GraphQL API | 41건 | A100 80GB PCIe ($1.390/h), A100 SXM4 ($1.490/h), MI300X ($2.390/h) |
| **AWS EC2** | https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-northeast-2/index.json | AWS Pricing JSON API | 52건 | A100 40GB ($3.801/h), V100 ($4.234/h), A10G ($1.997/h) |
| **VESSL AI** | https://vessl.ai/ko/pricing | Playwright Stealth Scraper | 4건 | H100 SXM ($2.390/h), A100 SXM ($1.550/h), A100 PCIe ($1.100/h) |
| **GPUaaS (국내)** | https://gpuaas.kr/ | Playwright HTML Scraper | 3건 | H100 SXM ($2.390/h), A100 SXM ($1.550/h), L40S ($1.800/h) |
| **CloudV (국내)** | https://cloudv.kr/server/gpu.html | Playwright HTML Scraper | 4건 | A100 40GB ($0.350/h), A100 80GB ($0.420/h), RTX 4090 ($0.150/h) |
| **RunYourAI (국내)** | https://console.runyour.ai/gpu-cloud | Playwright HTML Scraper | 3건 | H100 ($2.400/h), A100 ($1.600/h), RTX 4090 ($0.350/h) |
| **Gabia (가비아)** | https://www.gabia.com/ | Playwright HTML Scraper | 2건 | A100 80GB ($0.850/h), V100 ($0.400/h) |
| **KT Cloud (국내)** | https://cloud.kt.com/ | Playwright HTML Scraper | 3건 | H100 ($3.000/h), A100 ($1.900/h), V100 ($0.600/h) |

---

## 🔍 수집 및 정제 시스템 특징

1. **API 기반 직수집 (High Reliability):**
   - Vast.ai, Runpod, AWS는 공식 REST / GraphQL / Pricing JSON API 엔드포인트를 호출하여 직접 실측 데이터를 파싱합니다.
2. **웹 스크래핑 수집 (Playwright Stealth):**
   - Vessl, GPUaaS, CloudV, KT Cloud 등은 봇 차단을 우회하는 Playwright Headless Browser를 통해 실시간 웹 화면 단가를 파싱합니다.
3. **단위 정제 (Normalization):**
   - 멀티 GPU 인스턴스의 경우 개별 인스턴스 전체 가격을 GPU 개수로 나누어 **`1개 GPU당 1시간 단가 ($/h)`**로 통일 정제하여 데이터베이스에 저장합니다.
