from fastapi import APIRouter, Request
from typing import List, Any
from apps.server.core.data_service import data_service

router = APIRouter()

@router.get("/")
async def get_resources(request: Request) -> Any:
    """Return resources dynamically based on the API route prefix."""
    path = request.url.path
    
    if "/cpu" in path:
        return await data_service.get_cpus_for_ui()
    elif "/storage" in path:
        return await data_service.get_storages_for_ui()
    elif "/baremetal" in path:
        return await data_service.get_baremetals_for_ui()
    
    return []

