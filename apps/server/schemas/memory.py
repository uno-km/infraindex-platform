from pydantic import BaseModel, ConfigDict
import uuid
from typing import Optional

class MemoryModuleResponse(BaseModel):
    id: uuid.UUID
    manufacturer_id: str
    type: str
    capacity_gb: float
    speed_mhz: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)
