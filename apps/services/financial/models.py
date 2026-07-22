import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from apps.api.models.base import Base

class FinancialMarketHistory(Base):
    __tablename__ = "financial_market_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_type = Column(String(50), nullable=False, index=True)  # "stock", "future"
    symbol = Column(String(100), nullable=False, index=True)      # e.g., "NVDA", "DRAM_FUTURES"
    
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=True)  # Volume might be null for some indices/futures
    
    currency = Column(String(10), nullable=False, default="USD") # USD, KRW
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    
    def __repr__(self) -> str:
        return f"<FinancialMarketHistory(asset_type={self.asset_type}, symbol={self.symbol}, close={self.close}, timestamp={self.timestamp})>"
