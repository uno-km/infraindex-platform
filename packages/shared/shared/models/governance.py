from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from shared.models.base import Base, UUIDMixin, TimeStampMixin

class DataLicense(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "data_licenses"
    
    name: Mapped[str] = mapped_column(String(255))
    version: Mapped[str | None] = mapped_column(String(50))
    collection_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    public_display_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    redistribution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    attribution_required: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str | None] = mapped_column(Text)

class SourceAttribution(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "source_attributions"
    
    provider_id: Mapped[str] = mapped_column(String(255), index=True)
    license_id: Mapped[str] = mapped_column(ForeignKey("data_licenses.id"))
    attribution_text: Mapped[str] = mapped_column(Text)
    official_source_url: Mapped[str] = mapped_column(String(1024))
