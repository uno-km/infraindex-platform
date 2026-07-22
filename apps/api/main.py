from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from apps.api.api.v1.api import api_router
from apps.api.api.v1.endpoints import admin
from apps.api.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Global Infrastructure Price Intelligence Platform API",
    version=settings.VERSION,
)

# TODO: Configure proper CORS origins for production instead of allowing all
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Observability: Add Prometheus metrics instrumentation
Instrumentator().instrument(app).expose(app)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "infraindex-api"}

@app.get("/")
def root():
    return {"message": "Welcome to InfraIndex API"}
