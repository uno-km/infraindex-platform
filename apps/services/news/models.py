from sqlalchemy import String, DateTime, Text, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from apps.api.models.base import Base, UUIDMixin


class NewsArticle(Base, UUIDMixin):
    """
    글로벌 IT/반도체 뉴스 데이터 테이블
    """
    __tablename__ = "news_articles"

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), unique=True, index=True, nullable=False) # URL로 중복 방지
    source: Mapped[str] = mapped_column(String(100), index=True, nullable=False) # e.g. "Google News", "YouTube", "Bloomberg"
    
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    keywords: Mapped[str | None] = mapped_column(String(500), nullable=True) # 콤마 분리된 키워드 등
    collection_tier: Mapped[str | None] = mapped_column(String(50), nullable=True, default="tier1_rss") # e.g. "tier1_rss", "tier2_api", "tier3_scraper"
    
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )

    __table_args__ = (
        # 최신 뉴스 조회를 위한 인덱스
        Index(
            "ix_news_articles_published_at_source",
            "published_at", "source"
        ),
    )
