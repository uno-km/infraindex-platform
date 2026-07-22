from pydantic import BaseModel, ConfigDict
from typing import Optional, List
import uuid

class GpuVariantBase(BaseModel):
    name: str
    form_factor: Optional[str] = None
    vram_gb: float

class GpuVariantResponse(GpuVariantBase):
    id: uuid.UUID
    model_id: str
    
    model_config = ConfigDict(from_attributes=True)

class GpuModelBase(BaseModel):
    name: str

class GpuModelResponse(GpuModelBase):
    id: uuid.UUID
    manufacturer_id: str
    variants: List[GpuVariantResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class GpuManufacturerBase(BaseModel):
    name: str

class GpuManufacturerResponse(GpuManufacturerBase):
    id: uuid.UUID
    models: List[GpuModelResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
