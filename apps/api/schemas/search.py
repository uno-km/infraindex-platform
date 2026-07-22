from pydantic import BaseModel
from typing import Optional, List
from apps.api.schemas.offer import PricingPlanResponse

class SearchRequest(BaseModel):
    query: Optional[str] = None
    provider_slugs: Optional[List[str]] = None
    gpu_models: Optional[List[str]] = None
    min_vram_gb: Optional[float] = None
    max_price_hourly: Optional[float] = None
    plan_types: Optional[List[str]] = None # on_demand, spot, etc.
    sort_by: Optional[str] = "price_asc"
    
class SearchResponse(BaseModel):
    results: List[PricingPlanResponse]
    total: int
    page: int
    size: int
