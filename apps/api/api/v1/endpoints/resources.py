from fastapi import APIRouter
from typing import List

router = APIRouter()

@router.get("/")
async def get_dummy_resources():
    """Return an empty list for unimplemented resource categories."""
    return []
