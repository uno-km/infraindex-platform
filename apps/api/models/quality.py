from sqlalchemy import String, Integer, Text, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from apps.api.models.base import Base, UUIDMixin, TimeStampMixin
from datetime import datetime
from typing import Optional


class CollectionRun(Base, UUIDMixin, TimeStampMixin):
    """
    수집 실행 로그.

    provider_id: UUID FK 제거 → slug String.
      이유: providers 테이블에 seed 데이터 없어도 worker가 바로 INSERT 가능.
           FK 위반으로 수집 로그 자체가 실패하는 상황 방지.
    error_message: 실패 시 예외 메시지 기록.
    """
    __tablename__ = "collection_runs"

    # providers.id FK 제거 → slug 기반 (예: "vast-ai", "runpod")
    provider_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # success | failed | partial
    items_collected: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_collection_runs_provider_started", "provider_id", "started_at"),
    )


class DataQualityIssue(Base, UUIDMixin, TimeStampMixin):
    """
    데이터 품질 이슈 기록.

    run_id: nullable=True — CollectionRun 없이도 독립 기록 가능.
      (예: 단위 테스트, 수동 데이터 업로드)
    """
    __tablename__ = "data_quality_issues"

    # nullable: CollectionRun 없어도 이슈 기록 가능
    run_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    observation_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    issue_type: Mapped[str] = mapped_column(String(100), nullable=False)  # negative_price | missing_field | extreme_variance
    severity: Mapped[str] = mapped_column(String(50), nullable=False)      # quarantine | warning | info
    description: Mapped[str] = mapped_column(Text, nullable=False)
    # 원시 데이터 스냅샷 (JSON 문자열) — 재검토 시 원본 확인용
    raw_data_snapshot: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

