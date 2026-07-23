from sqlalchemy import String, DateTime, Text, Index, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from apps.api.models.base import Base, UUIDMixin


class NewsArticle(Base, UUIDMixin):
    """
    글로벌 IT/반도체 뉴스 데이터 테이블
    - tbl_news_arti
    """
    __tablename__ = "tbl_news_arti"

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), unique=True, index=True, nullable=False) 
    canonical_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    source_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False) # e.g. "Google News", "YouTube"
    source_domain: Mapped[str | None] = mapped_column(String(100), nullable=True)
    author: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    language: Mapped[str | None] = mapped_column(String(10), nullable=True, default="en")
    content_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False, default="article") # article or youtube
    
    is_semiconductor_related: Mapped[bool] = mapped_column(Boolean, default=False)
    category: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)
    categories: Mapped[list | dict | None] = mapped_column(JSON, nullable=True) # 다중 카테고리
    matched_keywords: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    collection_tier: Mapped[str | None] = mapped_column(String(50), nullable=True, default="tier1_rss")
    metadata_json: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        Index(
            "idx_news_arti_pub_src",
            "published_at", "source_name"
        ),
    )
