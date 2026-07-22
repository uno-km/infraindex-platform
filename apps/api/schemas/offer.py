from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
import uuid
from apps.api.schemas.provider import ProviderResponse, ProviderRegionResponse
from apps.api.schemas.gpu import GpuVariantResponse

class OfferingGpuConfigurationResponse(BaseModel):
    id: uuid.UUID
    count: int
    variant: GpuVariantResponse
    
    model_config = ConfigDict(from_attributes=True)

class InstanceOfferingResponse(BaseModel):
    id: uuid.UUID
    machine_type_name: str
    includes_cpu: bool
    includes_ram: bool
    includes_local_storage: bool
    
    provider: ProviderResponse
    region: Optional[ProviderRegionResponse] = None
    gpu_configuration: List[OfferingGpuConfigurationResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class PriceObservationResponse(BaseModel):
    id: uuid.UUID
    source_price: float
    source_currency: str
    source_unit: str
    normalized_hourly_price: float
    normalized_gpu_hour_price: float
    normalized_vram_gb_hour_price: float
    normalized_monthly_price: float
    availability_status: str
    collected_at: datetime
    source_url: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class PricingPlanResponse(BaseModel):
    id: uuid.UUID
    plan_type: str
    billing_increment_seconds: int
    minimum_billing_seconds: int
    
    offering: InstanceOfferingResponse
    observations: List[PriceObservationResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
