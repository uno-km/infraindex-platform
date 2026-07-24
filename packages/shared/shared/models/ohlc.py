from sqlalchemy import String, DateTime, Date, Numeric, Boolean, Index, ForeignKey, Float, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime, date
import uuid

from shared.models.base import Base, UUIDMixin
from shared.models.market import MarketProduct  # noqa: reuse FK ref


class MarketOHLCDaily(Base, UUIDMixin):
    """
    리테일 시장 일별 OHLC (Open/High/Low/Close) 집계 테이블.
    tbl_market_price_obs 의 관측치를 일 단위로 집계하여 캔들스틱 차트에 사용.
    """
    __tablename__ = "tbl_market_ohlc_daily"

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tbl_market_product.id", ondelete="CASCADE"), index=True, nullable=False
    )
    trade_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    open_price: Mapped[float] = mapped_column(Float, nullable=False)    # 해당일 첫 관측 가격
    high_price: Mapped[float] = mapped_column(Float, nullable=False)    # 해당일 최고가
    low_price: Mapped[float] = mapped_column(Float, nullable=False)     # 해당일 최저가
    close_price: Mapped[float] = mapped_column(Float, nullable=False)   # 해당일 마지막 관측 가격
    avg_price: Mapped[float | None] = mapped_column(Float)              # 해당일 평균가

    volume: Mapped[int] = mapped_column(Integer, default=0)             # 수집 포인트 수
    vendor_count: Mapped[int] = mapped_column(Integer, default=0)       # 참여 판매처 수

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    product: Mapped["MarketProduct"] = relationship("MarketProduct")

    __table_args__ = (
        UniqueConstraint("product_id", "trade_date", name="uq_ohlc_product_date"),
        Index("idx_ohlc_product_date", "product_id", "trade_date"),
    )
