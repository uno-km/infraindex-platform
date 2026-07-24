from datetime import date, datetime
from sqlalchemy import String, Float, Boolean, Date, DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from shared.models.base import Base, UUIDMixin

class AIModelMaster(Base, UUIDMixin):
    """
    AI 모델 마스터 정보 (Tier, 제조사, 모델명 등)
    """
    __tablename__ = "tbl_ai_model_master"

    model_code: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False, comment="OpenRouter 모델 코드 (예: openai/gpt-4o)")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="표시할 모델명")
    provider: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="제조사 (OpenAI, Anthropic 등)")
    tier: Mapped[str] = mapped_column(String(20), index=True, nullable=False, comment="성능 체급 (Tier 0 ~ Tier 3)")
    context_length: Mapped[int | None] = mapped_column(nullable=True, comment="지원하는 컨텍스트 윈도우 크기")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    history: Mapped[list["AIModelPriceHistory"]] = relationship("AIModelPriceHistory", back_populates="model_master", cascade="all, delete-orphan")


class AIModelPriceHistory(Base, UUIDMixin):
    """
    매일 수집되는 AI 모델 가격 정보 (시계열)
    """
    __tablename__ = "tbl_ai_model_price_history"

    model_id: Mapped[str] = mapped_column(ForeignKey("tbl_ai_model_master.id", ondelete="CASCADE"), index=True, nullable=False)
    collected_date: Mapped[date] = mapped_column(Date, index=True, nullable=False, default=func.current_date(), comment="수집 일자 (선차트 x축)")
    
    # Prices are generally extremely small (e.g., $0.00000015 per token), 
    # but OpenRouter API gives them per token. 
    # We will store them normalized per 1M tokens for readability and chart plotting.
    input_price_1m: Mapped[float] = mapped_column(Float, nullable=False, comment="100만 토큰 당 Input 가격 (USD)")
    output_price_1m: Mapped[float] = mapped_column(Float, nullable=False, comment="100만 토큰 당 Output 가격 (USD)")
    
    # Optional fields like cache pricing if we ever scrape it.
    cached_input_price_1m: Mapped[float | None] = mapped_column(Float, nullable=True, comment="100만 토큰 당 Cached Input 가격 (USD)")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    model_master: Mapped["AIModelMaster"] = relationship("AIModelMaster", back_populates="history")

    __table_args__ = (
        Index("idx_ai_model_price_hist_unique", "model_id", "collected_date", unique=True),
    )
