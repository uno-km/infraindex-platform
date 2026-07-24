from sqlalchemy import String, Boolean, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from shared.models.base import Base, UUIDMixin

class CrawlerConfig(Base, UUIDMixin):
    """
    크롤러 동적 제어 테이블 (하드코딩 제거)
    이 테이블의 값을 읽어 Celery가 수집 주기를 결정하고, 크롤러가 타겟을 결정합니다.
    """
    __tablename__ = "crawler_configs"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True) # e.g. "news_tier1_rss"
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # 주기 (Crontab format or minute interval)
    interval_minutes: Mapped[int] = mapped_column(Integer, default=60)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # 타겟 URL들 (JSON List 형태로 저장하거나 별도 테이블로 뺄 수 있음. 여기서는 편의상 쉼표로 구분)
    target_urls: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
