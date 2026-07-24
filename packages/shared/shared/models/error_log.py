from sqlalchemy import String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from shared.models.base import Base, UUIDMixin

class ErrorLog(Base, UUIDMixin):
    """
    시스템에서 발생하는 예외(Exception)를 수집하는 로그 테이블.
    매일 오전 8시에 배치 워커가 미발송(is_sent=False) 에러를 모아 LLM으로 요약 후 텔레그램 발송.
    """
    __tablename__ = "tbl_error_log"

    severity: Mapped[str] = mapped_column(String(20), index=True, default="NORMAL", comment="CRITICAL, NORMAL, LOW")
    source: Mapped[str] = mapped_column(String(100), index=True, comment="어디서 에러가 났는지 (e.g. ai_pricing_crawler)")
    error_type: Mapped[str] = mapped_column(String(100), comment="Exception 클래스 이름")
    error_message: Mapped[str] = mapped_column(Text, comment="에러 메시지")
    traceback: Mapped[str | None] = mapped_column(Text, nullable=True, comment="스택 트레이스")
    context_data: Mapped[str | None] = mapped_column(Text, nullable=True, comment="발생 당시의 변수나 추가 정보(JSON)")
    
    is_sent: Mapped[bool] = mapped_column(Boolean, default=False, index=True, comment="텔레그램 발송 여부")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
