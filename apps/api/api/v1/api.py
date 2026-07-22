from fastapi import APIRouter
from apps.api.api.v1.endpoints import providers, gpus, search, history, admin, memory, storage, chat, chart, stream, health, reports, traffic, resources

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(providers.router, prefix="/providers", tags=["providers"])
api_router.include_router(gpus.router, prefix="/gpus", tags=["gpus"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
api_router.include_router(memory.router, prefix="/memory", tags=["memory"])
api_router.include_router(storage.router, prefix="/storage", tags=["storage"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(chart.router, prefix="/chart", tags=["chart"])
api_router.include_router(stream.router, prefix="/stream", tags=["stream"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(traffic.router, prefix="/traffic", tags=["traffic"])
api_router.include_router(resources.router, prefix="/cpu", tags=["cpu"])
api_router.include_router(resources.router, prefix="/storage", tags=["storage"])
api_router.include_router(resources.router, prefix="/baremetal", tags=["baremetal"])
