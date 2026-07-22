from fastapi import APIRouter, Request
from typing import List

from apps.api.core.data_service import data_service

router = APIRouter()

@router.get("/")
async def get_resources(request: Request):
    """Return resources. Handled CPU if prefix is /cpu."""
    if "cpu" in request.url.path:
        return await data_service.get_cpus_for_ui()
    return []
