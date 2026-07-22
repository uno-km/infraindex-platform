from pydantic import BaseModel, ConfigDict
import uuid

class StorageTierResponse(BaseModel):
    id: uuid.UUID
    provider_id: str
    name: str
    price_per_gb_month: float
    egress_price_per_gb: float
    
    model_config = ConfigDict(from_attributes=True)
