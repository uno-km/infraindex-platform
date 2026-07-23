from sqlalchemy import String, DateTime, Text, Index
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

    titl_nm: Mapped[str] = mapped_column(String(500), nullable=False)
    arti_url: Mapped[str] = mapped_column(String(1000), unique=True, index=True, nullable=False) # URL로 중복 방지
    src_nm: Mapped[str] = mapped_column(String(100), index=True, nullable=False) # e.g. "Google News", "YouTube", "Bloomberg"
    
    pub_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    sum_txt: Mapped[str | None] = mapped_column(Text, nullable=True)
    kwd_txt: Mapped[str | None] = mapped_column(String(500), nullable=True) # 콤마 분리된 키워드 등
    clct_tr: Mapped[str | None] = mapped_column(String(50), nullable=True, default="tier1_rss") # e.g. "tier1_rss", "tier2_api", "tier3_scraper"
    
    crt_ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True, nullable=False
    )

    __table_args__ = (
        Index(
            "idx_news_arti_pub_src",
            "pub_ts", "src_nm"
        ),
    )

