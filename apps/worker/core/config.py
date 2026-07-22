from pydantic_settings import BaseSettings

class WorkerSettings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # DB (Same as API, used if workers write directly to DB instead of via API)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "infraindex"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "infraindex"
    POSTGRES_PORT: str = "5432"
    
    # Circuit Breaker defaults
    CB_FAILURE_THRESHOLD: int = 5
    CB_RECOVERY_TIMEOUT: int = 60
    
    class Config:
        env_file = ".env"

settings = WorkerSettings()
