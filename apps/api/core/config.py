import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "infraindex-platform API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "infraindex"
    POSTGRES_PASSWORD: str = "password"
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

    # Redis (For Caching / Worker)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
