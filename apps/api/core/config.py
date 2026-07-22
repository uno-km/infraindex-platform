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

    # FIX-03: Database - 기본 비밀번호 제거. 미설정 시 시작 실패.
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "infraindex"
    POSTGRES_PASSWORD: str  # 기본값 없음 → env 필수
    POSTGRES_DB: str = "infraindex"
    POSTGRES_PORT: str = "5432"

    @property
    def sync_database_uri(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def async_database_uri(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # ---------------------------------------------------------
    # 🎯 FEATURE FLAGS (Loose Coupling / Environment Switching)
    # ---------------------------------------------------------
    USE_REAL_DB: bool = os.environ.get("USE_REAL_DB", "False").lower() == "true"
    LOCAL_STORAGE_DIR: str = os.path.join(os.getcwd(), "data")

    # Redis (For Caching / Worker / Rate Limiting)
    REDIS_URL: str = "redis://localhost:6379/0"

    # FIX-01: Admin API 인증용 API Key
    # 미설정 시 admin 엔드포인트가 503을 반환하여 무방비 노출 방지
    ADMIN_API_KEY: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
