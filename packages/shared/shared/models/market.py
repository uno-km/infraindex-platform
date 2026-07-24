from sqlalchemy import String, DateTime, Numeric, Boolean, Index, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

from shared.models.base import Base, UUIDMixin

class MarketProduct(Base, UUIDMixin):
    """표준화된 상품 마스터 엔터티"""
    __tablename__ = "tbl_market_product"

    manufacturer: Mapped[str] = mapped_column(String(100), index=True) # NVIDIA, AMD
    model_name: Mapped[str] = mapped_column(String(200), index=True)   # RTX 4090
    product_line: Mapped[str | None] = mapped_column(String(100))      # GeForce
    category: Mapped[str] = mapped_column(String(50), index=True)      # GPU, CPU, RAM
    generation: Mapped[str | None] = mapped_column(String(50))         # Ada Lovelace
    vram_gb: Mapped[float | None] = mapped_column(Float)
    memory_type: Mapped[str | None] = mapped_column(String(50))        # GDDR6X
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    listings: Mapped[list["MarketListing"]] = relationship("MarketListing", back_populates="product", cascade="all, delete-orphan")


class MarketListing(Base, UUIDMixin):
    """각 판매처(Vendor)의 실제 등록 상품"""
    __tablename__ = "tbl_market_listing"

    product_id: Mapped[str] = mapped_column(ForeignKey("tbl_market_product.id", ondelete="CASCADE"), index=True)
    vendor_name: Mapped[str] = mapped_column(String(100), index=True) # Naver, Amazon, 11st
    original_title: Mapped[str] = mapped_column(String(500))
    url: Mapped[str] = mapped_column(String(1000), unique=True, index=True)
    condition: Mapped[str] = mapped_column(String(20), default="new") # new, used, refurbished
    country: Mapped[str] = mapped_column(String(10), default="KR")
    currency: Mapped[str] = mapped_column(String(10), default="KRW")
    
    product: Mapped["MarketProduct"] = relationship("MarketProduct", back_populates="listings")
    observations: Mapped[list["MarketPriceObservation"]] = relationship("MarketPriceObservation", back_populates="listing", cascade="all, delete-orphan")


class MarketPriceObservation(Base, UUIDMixin):
    """시계열 가격 수집 관측치 (시계열 데이터베이스 형태)"""
    __tablename__ = "tbl_market_price_obs"

    listing_id: Mapped[str] = mapped_column(ForeignKey("tbl_market_listing.id", ondelete="CASCADE"), index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    shipping_fee: Mapped[float] = mapped_column(Float, default=0.0)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="KRW")
    
    # 환율 반영 달러 환산가
    price_usd: Mapped[float | None] = mapped_column(Float)
    
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    listing: Mapped["MarketListing"] = relationship("MarketListing", back_populates="observations")

    __table_args__ = (
        Index("idx_market_obs_listing_time", "listing_id", "observed_at"),
    )


class MarketRentalOffer(Base, UUIDMixin):
    """클라우드 및 대여 인스턴스 가격"""
    __tablename__ = "tbl_market_rental"

    provider: Mapped[str] = mapped_column(String(100), index=True) # AWS, Vast.ai
    instance_name: Mapped[str] = mapped_column(String(200), index=True)
    hardware_model: Mapped[str] = mapped_column(String(200), index=True) # H100, RTX 4090
    
    hourly_price: Mapped[float] = mapped_column(Float, nullable=False)
    monthly_price: Mapped[float | None] = mapped_column(Float) # hourly * 730
    
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    region: Mapped[str | None] = mapped_column(String(100))
    is_contract: Mapped[bool] = mapped_column(Boolean, default=False) # On-demand vs Reserved
    
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (
        Index("idx_market_rental_hw_time", "hardware_model", "observed_at"),
    )
