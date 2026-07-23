from apps.api.models.base import Base
from apps.api.models.observation import PriceObservation
from apps.api.models.quality import CollectionRun, DataQualityIssue
from apps.api.models.governance import DataLicense, SourceAttribution
from apps.api.models.alert import PriceAlert
from apps.api.models.memory import MemoryManufacturer, MemoryModule
from apps.api.models.storage import StorageProvider, StorageTier
from apps.api.models.scheduler import ScheduleConfig, IdempotencyKey
from apps.api.models.outbox import OutboxEvent
from apps.api.models.system_code import SystemCodeGroup, SystemCode

# Import domain models to register them with Base.metadata for Alembic
from apps.services.gpu.models_history import GpuPriceHistory
from apps.services.gpu.models_hardware import GpuManufacturer, GpuModel, GpuVariant, CpuManufacturer, CpuModel, CpuVariant
from apps.services.gpu.models_provider import Provider, ProviderRegion
from apps.services.gpu.models_offering import InstanceOffering, OfferingGpuConfiguration, OfferingCpuConfiguration, PricingPlan
from apps.services.retail.models import RtlPriceHistory
from apps.services.financial.models import FinMktHistory
from apps.services.news.models import NewsArticle

__all__ = ["Base", "CollectionRun", "DataQualityIssue", "OutboxEvent", "SystemCodeGroup", "SystemCode", "GpuPriceHistory", "RtlPriceHistory", "FinMktHistory", "NewsArticle"]
