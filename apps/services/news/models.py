from sqlalchemy import String, DateTime, Text, Index, Boolean, JSON, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

from apps.api.models.base import Base, UUIDMixin


class NewsSource(Base, UUIDMixin):
    """
    뉴스/미디어 출처 및 메타데이터
    - 언론사, YouTube 채널, 블로그 등
    """
    __tablename__ = "tbl_news_source"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_type: Mapped[str] = mapped_column(String(50), default="media")  # media, youtube, blog, etc
    country: Mapped[str | None] = mapped_column(String(10), default="US")
    language: Mapped[str | None] = mapped_column(String(10), default="en")
    
    reliability_score: Mapped[float] = mapped_column(Float, default=1.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    articles: Mapped[list["NewsArticle"]] = relationship("NewsArticle", back_populates="source")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class NewsTag(Base, UUIDMixin):
    """
    뉴스 태그 및 키워드 마스터 테이블
    """
    __tablename__ = "tbl_news_tag"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True) # e.g., AI, Semiconductor, Company
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class NewsArticleTag(Base, UUIDMixin):
    """
    뉴스 기사 - 태그 N:M 매핑 테이블
    """
    __tablename__ = "tbl_news_article_tag"

    article_id: Mapped[str] = mapped_column(ForeignKey("tbl_news_article.id", ondelete="CASCADE"), index=True, nullable=False)
    tag_id: Mapped[str] = mapped_column(ForeignKey("tbl_news_tag.id", ondelete="CASCADE"), index=True, nullable=False)
    
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True) # 자동 태깅 시 신뢰도 점수

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    
    __table_args__ = (
        Index("idx_article_tag_unique", "article_id", "tag_id", unique=True),
    )


class NewsArticle(Base, UUIDMixin):
    """
    글로벌 IT/반도체 뉴스 데이터 테이블
    """
    __tablename__ = "tbl_news_article"

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), unique=True, index=True, nullable=False) 
    canonical_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    
    source_id: Mapped[str | None] = mapped_column(ForeignKey("tbl_news_source.id", ondelete="SET NULL"), index=True, nullable=True)
    source: Mapped["NewsSource"] = relationship("NewsSource", back_populates="articles")
    
    # 레거시 호환 및 빠른 검색용 denormalized 필드
    source_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
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
    categories: Mapped[list | dict | None] = mapped_column(JSON, nullable=True) # 레거시 다중 카테고리
    matched_keywords: Mapped[str | None] = mapped_column(String(500), nullable=True) # 레거시 키워드
    
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
            "idx_news_article_pub_src",
            "published_at", "source_name"
        ),
    )

class NewsDailyBriefing(Base, UUIDMixin):
    """
    일일 뉴스 요약 리포트 (LLM 기반)
    """
    __tablename__ = "tbl_news_daily_briefing"

    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(50), index=True, nullable=False, default="전체")
    content: Mapped[str] = mapped_column(Text, nullable=False)
    model_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_article_ids: Mapped[list | dict | None] = mapped_column(JSON, nullable=True) # 요약에 쓰인 기사 ID들

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        Index("idx_briefing_date_cat", "date", "category", unique=True),
    )
