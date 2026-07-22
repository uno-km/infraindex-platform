from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.core.database import get_db

router = APIRouter()

@router.get("/{offering_id}")
async def get_price_history(
    offering_id: str,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get price history for a specific offering.
    """
    # TODO: Implement history logic
    return {"offering_id": offering_id, "history": []}
