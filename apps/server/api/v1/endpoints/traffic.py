from fastapi import APIRouter
from apps.server.core.traffic_service import traffic_service

router = APIRouter()

@router.post("/{resource_id}")
async def increment_traffic(resource_id: str):
    """Increment the view/click traffic count for a specific resource (e.g. GPU model)."""
    new_count = traffic_service.increment_view(resource_id)
    return {"resource_id": resource_id, "traffic_count": new_count}

@router.get("/")
async def get_traffic():
    """Get all traffic counts."""
    return traffic_service.get_all_traffic()
