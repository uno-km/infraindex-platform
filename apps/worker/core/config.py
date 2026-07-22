import os
from pydantic_settings import BaseSettings

class WorkerSettings(BaseSettings):
    # 전역 Feature Flags (Loose Coupling)
    USE_REAL_DB: bool = os.environ.get("USE_REAL_DB", "False").lower() == "true"
    USE_CELERY_QUEUE: bool = os.environ.get("USE_CELERY_QUEUE", "False").lower() == "true"
    ENABLE_ALERTS: bool = os.environ.get("ENABLE_ALERTS", "False").lower() == "true"
    USE_PROXY: bool = os.environ.get("USE_PROXY", "False").lower() == "true"
    
    # DB / Redis (Only used if flags are True)
    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
    
    # Local Storage path (for USE_REAL_DB=False)
    LOCAL_STORAGE_DIR: str = os.path.join(os.getcwd(), "data")

    class Config:
        env_file = ".env"

settings = WorkerSettings()
