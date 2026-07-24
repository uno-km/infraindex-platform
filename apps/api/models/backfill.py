"""
apps/api/models/backfill.py
Phase 8 - 히스토리컬 백필 Job 추적 모델

테이블:
  tbl_backfill_job — 백필 작업 상태 추적
  tbl_url_hash     — URL 해시 캐시 (중복 감지 최적화)
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column, Date, DateTime, Integer, String, Text, func
)

from apps.api.models.base import Base, UUIDMixin


class BackfillJob(UUIDMixin, Base):
    """
    히스토리컬 백필 작업 추적 테이블.
    
    status 값:
      - pending  : 생성됨, 아직 시작 안 함
      - running  : 실행 중
      - done     : 완료
      - failed   : 에러 발생
      - cancelled: 취소됨
    """
    __tablename__ = "tbl_backfill_job"

    source       = Column(String(100), nullable=False, comment="데이터 소스 (예: arxiv, sitemap_tomshardware)")
    from_date    = Column(Date, nullable=False, comment="백필 시작 날짜")
    to_date      = Column(Date, nullable=False, comment="백필 종료 날짜")
    status       = Column(String(20), default="pending", nullable=False, comment="pending/running/done/failed/cancelled")
    total_urls   = Column(Integer, default=0, comment="발견된 총 URL 수")
    processed    = Column(Integer, default=0, comment="처리된 URL 수")
    new_articles = Column(Integer, default=0, comment="새로 저장된 기사 수")
    started_at   = Column(DateTime(timezone=True), nullable=True, comment="작업 시작 시각")
    finished_at  = Column(DateTime(timezone=True), nullable=True, comment="작업 완료 시각")
    error_msg    = Column(Text, nullable=True, comment="에러 메시지 (failed 시)")
    created_at   = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 시각")

    def __repr__(self) -> str:
        return f"<BackfillJob id={self.id} source={self.source} status={self.status}>"

    @property
    def progress_pct(self) -> Optional[float]:
        """진행률 (0.0 ~ 100.0)"""
        if not self.total_urls or self.total_urls == 0:
            return None
        return round(self.processed / self.total_urls * 100, 1)

    @property
    def duration_seconds(self) -> Optional[float]:
        """소요 시간 (초). 완료/실패 시에만 반환"""
        if self.started_at and self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return None


class UrlHash(Base):
    """
    URL 해시 캐시 테이블.
    중복 감지 1차 체크를 DB 조회로 수행하기 위한 빠른 인덱스.
    """
    __tablename__ = "tbl_url_hash"

    url_hash   = Column(String(64), primary_key=True, comment="SHA-256(정규화된 URL)")
    source     = Column(String(100), nullable=True, comment="출처 도메인")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<UrlHash hash={self.url_hash[:16]}...>"
