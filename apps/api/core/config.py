import os
from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "infraindex-platform API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # FIX-02: CORS - 기본값 와일드카드 제거. 반드시 환경변수로 도메인 명시.
    # 로컬 개발: BACKEND_CORS_ORIGINS='["http://localhost:3000"]'
    BACKEND_CORS_ORIGINS: list[str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            import json
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass
            # 쉼표 구분도 허용
            return [o.strip() for o in v.split(",") if o.strip()]
        return v

    # FIX-03: Database Environments (Dev vs Prod)
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "dev") # 'dev' or 'prod'
    
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "infraindex"
    POSTGRES_PASSWORD: str = "testpass"  # Provided default for local dev
    POSTGRES_DB: str = "infraindex"
    POSTGRES_PORT: str = "5432"
    
    # Overrides for test DB
    TEST_POSTGRES_DB: str = "infraindex_test"

    @property
    def db_name(self) -> str:
        if self.ENVIRONMENT == "test":
            return self.TEST_POSTGRES_DB
        return self.POSTGRES_DB

    @property
    def sync_database_uri(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.db_name}"

    @property
    def async_database_uri(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.db_name}"

    # JWT Auth Config
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "super-secret-local-key")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 1 day

    # OAuth Config (Google, Naver, Kakao)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    NAVER_CLIENT_ID: Optional[str] = None
    NAVER_CLIENT_SECRET: Optional[str] = None
    KAKAO_CLIENT_ID: Optional[str] = None
    KAKAO_CLIENT_SECRET: Optional[str] = None

    # Retail Crawler API Keys
    NAVER_SHOPPING_CLIENT_ID: Optional[str] = None
    NAVER_SHOPPING_CLIENT_SECRET: Optional[str] = None
    COUPANG_ACCESS_KEY: Optional[str] = None
    COUPANG_SECRET_KEY: Optional[str] = None
    ELEVENSTREET_OPENAPI_KEY: Optional[str] = None

    # ---------------------------------------------------------
    # 🎯 FEATURE FLAGS (Loose Coupling / Environment Switching)
    # ---------------------------------------------------------
    USE_REAL_DB: bool = os.environ.get("USE_REAL_DB", "False").lower() == "true"
    LOCAL_STORAGE_DIR: str = os.path.join(os.getcwd(), "data")

    # Redis (For Caching / Worker / Rate Limiting)
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_MAX_CONNECTIONS: int = 50  # 전역 ConnectionPool 최대 연결 수

    # DB Connection Pool 튜닝
    # Render starter: CPU 0.5코어 → pool_size=5 권장
    # 자체 서버 배포: pool_size=10~20 권장
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 1800  # 30분마다 커넥션 갱신

    # 보안: Trusted Hosts (TrustedHostMiddleware)
    # 쉼표 구분 또는 JSON 배열로 주입
    # 예: TRUSTED_HOSTS='["myapp.onrender.com", "localhost"]'
    # 빈 리스트 = TrustedHostMiddleware 비활성화 (개발 편의)
    TRUSTED_HOSTS: list[str] = []

    @field_validator("TRUSTED_HOSTS", mode="before")
    @classmethod
    def parse_trusted_hosts(cls, v):
        if isinstance(v, str):
            import json
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass
            return [h.strip() for h in v.split(",") if h.strip()]
        return v

    # FIX-01: Admin API 인증용 API Key
    # 미설정 시 admin 엔드포인트가 503을 반환하여 무방비 노출 방지
    ADMIN_API_KEY: Optional[str] = None

    # P3-001: LLM API Keys (Chat NLP 엔진)
    OPENAI_API_KEY: Optional[str] = None   # GPT-4o-mini 사용 시 필요
    GEMINI_API_KEY: Optional[str] = None   # Gemini Flash 폴백 시 필요

    class Config:
        case_sensitive = True
        extra = "ignore"
        # 초기화 시점에 동적으로 결정되도록 함수에서 주입

@lru_cache()
def get_settings() -> Settings:
    # 1. OS 환경변수에서 ENVIRONMENT 확인 (기본값 local)
    env_state = os.environ.get("ENVIRONMENT", "local").lower()
    
    # 2. 상태에 맞는 .env 파일 매핑
    env_file = ".env" # fallback
    if env_state in ("prd", "prod", "production"):
        env_file = ".env.prd" if os.path.exists(".env.prd") else ".env.production"
    elif env_state in ("dev", "staging"):
        env_file = ".env.staging" if os.path.exists(".env.staging") else ".env.dev"
    elif env_state in ("local", "dev_local"):
        env_file = ".env.local"
        
    # 만약 매핑된 파일이 없으면 기본 .env 사용
    if not os.path.exists(env_file):
        env_file = ".env"
        
    return Settings(_env_file=env_file, _env_file_encoding="utf-8")

settings = get_settings()
