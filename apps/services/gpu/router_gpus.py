from typing import Any, List
from fastapi import APIRouter
from apps.api.core.data_service import data_service

router = APIRouter()

@router.get("/")
async def read_gpus() -> Any:
    """
    Retrieve GPU models with their variants and aggregated offers.
    Automatically switches between DB and JSON modes.
    """
    gpus = await data_service.get_gpus_for_ui()
    return gpus
