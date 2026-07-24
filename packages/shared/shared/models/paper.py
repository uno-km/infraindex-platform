from sqlalchemy import String, DateTime, Text, Index, Boolean, JSON, ForeignKey, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime, date

from shared.models.base import Base, UUIDMixin

class PaperSource(Base, UUIDMixin):
    """
    논문 출처 마스터 (e.g., arxiv, semantic_scholar)
    """
    __tablename__ = "tbl_paper_source"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    articles: Mapped[list["PaperArticle"]] = relationship("PaperArticle", back_populates="source_rel")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class PaperTag(Base, UUIDMixin):
    """
    논문 태그 (e.g., LLM, Transformer)
    """
    __tablename__ = "tbl_paper_tag"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    category: Mapped[str | None] = mapped_column(String(50)) 
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class PaperArticleTag(Base, UUIDMixin):
    """
    논문 - 태그 N:M 매핑
    """
    __tablename__ = "tbl_paper_article_tag"

    article_id: Mapped[str] = mapped_column(ForeignKey("tbl_paper_article.id", ondelete="CASCADE"), index=True, nullable=False)
    tag_id: Mapped[str] = mapped_column(ForeignKey("tbl_paper_tag.id", ondelete="CASCADE"), index=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        Index("idx_paper_article_tag_unique", "article_id", "tag_id", unique=True),
    )


class PaperArticle(Base, UUIDMixin):
    """
    논문 메타데이터 (JSONB 활용하여 유연하게 데이터 저장)
    """
    __tablename__ = "tbl_paper_article"

    external_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False) # e.g., "arxiv:2501.12345"
    source: Mapped[str] = mapped_column(String(50), index=True) # "arxiv"
    
    source_id: Mapped[str | None] = mapped_column(ForeignKey("tbl_paper_source.id", ondelete="SET NULL"), index=True)
    source_rel: Mapped["PaperSource"] = relationship("PaperSource", back_populates="articles")

    title: Mapped[str] = mapped_column(Text, nullable=False)
    title_ko: Mapped[str | None] = mapped_column(Text)
    
    published_at: Mapped[date | None] = mapped_column(Date, index=True)
    
    category: Mapped[str | None] = mapped_column(String(100), index=True)
    language: Mapped[str | None] = mapped_column(String(10), default="en")
    
    citation_count: Mapped[int] = mapped_column(Integer, default=0)
    is_analyzed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # MongoDB 대체: 원본 데이터 및 유연한 메타데이터 보관
    metadata_json: Mapped[dict | list | None] = mapped_column(JSON)
    # metadata_json 구조 예시:
    # {
    #   "authors": ["John Doe", "Jane Smith"],
    #   "abstract": "We investigate...",
    #   "abstract_ko": "본 논문에서는...",
    #   "url": "https://arxiv.org/abs/2501.12345",
    #   "pdf_url": "https://arxiv.org/pdf/2501.12345",
    #   "categories": ["cs.AI", "cs.LG"],
    #   "ai_analysis": { ... }
    # }

    crawled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_paper_article_pub_src", "published_at", "source"),
    )
