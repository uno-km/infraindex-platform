from fastapi import APIRouter
from apps.api.api.v1.endpoints import search, history, admin, memory, storage, chat, chart, stream, health, reports, traffic, auth, users, market

# Imported from Domain Services
from apps.services.gpu import router_providers as providers
from apps.services.gpu import router_gpus as gpus
from apps.services.cpu.router import router as cpu_router
from apps.services.retail.router import router as retail_charts_router
from apps.services.financial.router import router as insights_router
from apps.services.news.router import router as news_router
from apps.services.market.endpoints_retail_chart import router as retail_ohlc_router

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(providers.router, prefix="/providers", tags=["providers"])
api_router.include_router(gpus.router, prefix="/gpus", tags=["gpus"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
api_router.include_router(memory.router, prefix="/memory", tags=["memory"])
# api_router.include_router(storage.router, prefix="/storage", tags=["storage"])  # Replaced by cpu_router curated data
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(chart.router, prefix="/chart", tags=["chart"])
api_router.include_router(stream.router, prefix="/stream", tags=["stream"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(traffic.router, prefix="/traffic", tags=["traffic"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

# CPU/Baremetal (formerly resources)
api_router.include_router(cpu_router, prefix="/cpu", tags=["cpu"])
api_router.include_router(cpu_router, prefix="/storage", tags=["storage"])
api_router.include_router(cpu_router, prefix="/baremetal", tags=["baremetal"])

# Retail, Insights, News
api_router.include_router(retail_charts_router, prefix="/retail", tags=["retail"])
api_router.include_router(retail_ohlc_router, prefix="/retail", tags=["retail-ohlc"])
api_router.include_router(insights_router, prefix="/insights", tags=["insights"])
api_router.include_router(news_router, prefix="/news", tags=["news"])
api_router.include_router(market.router, prefix="/market", tags=["market"])
