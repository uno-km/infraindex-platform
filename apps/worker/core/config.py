from pydantic_settings import BaseSettings

class WorkerSettings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # DB (Same as API, used if workers write directly to DB instead of via API)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "infraindex"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "infraindex"
    POSTGRES_PORT: str = "5432"
    
    # ---------------------------------------------------------
    # 🎯 FEATURE FLAGS (Loose Coupling / Environment Switching)
    # ---------------------------------------------------------
    # If False, drops JSON files locally (Zero cost serverless mode). If True, saves to PostgreSQL.
    USE_REAL_DB: bool = False
    
    # If False, runs synchronously like a normal script. If True, dispatches to Redis/Celery queue.
    USE_CELERY_QUEUE: bool = False
    
    # If False, logs to console only. If True, sends Discord/Telegram Webhooks.
    ENABLE_ALERTS: bool = False
    
    # If False, uses local IP. If True, routes traffic through rotating proxy lists.
    USE_PROXY: bool = False
    
    # Circuit Breaker defaults
    CB_FAILURE_THRESHOLD: int = 5
    CB_RECOVERY_TIMEOUT: int = 60
    
    class Config:
        env_file = ".env"

settings = WorkerSettings()
