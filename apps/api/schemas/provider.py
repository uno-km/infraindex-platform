from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
import uuid

class ProviderRegionBase(BaseModel):
    provider_region_id: str
    name: str
    country: Optional[str] = None

class ProviderRegionResponse(ProviderRegionBase):
    id: uuid.UUID
    provider_id: str
    
    model_config = ConfigDict(from_attributes=True)

class ProviderBase(BaseModel):
    name: str
    slug: str
    official_homepage: Optional[str] = None
    is_active: bool = True

class ProviderResponse(ProviderBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ProviderDetailResponse(ProviderResponse):
    regions: List[ProviderRegionResponse] = []
