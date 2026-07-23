from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List

from apps.api.models.base import Base

class SystemCodeGroup(Base):
    """
    SYS_CD_GROUP_BAS: 시스템 코드 그룹 기준 테이블 (UPPERCASE 강제)
    """
    __tablename__ = "SYS_CD_GROUP_BAS"

    SYS_GROUP_ID: Mapped[str] = mapped_column(String(50), primary_key=True)
    GRP_NM: Mapped[str] = mapped_column(String(100), nullable=False)
    CRT_DT: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    UPD_DT: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    DESC_TXT: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    REF_VAL_1: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_2: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_3: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_4: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_5: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_6: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_7: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_8: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_9: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_10: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Relationship to SYS_CD_BAS
    system_codes: Mapped[List["SystemCode"]] = relationship(
        "SystemCode", back_populates="group", cascade="all, delete-orphan"
    )


class SystemCode(Base):
    """
    SYS_CD_BAS: 시스템 코드 기준 테이블 (UPPERCASE 강제)
    """
    __tablename__ = "SYS_CD_BAS"

    SYS_GROUP_ID: Mapped[str] = mapped_column(String(50), ForeignKey("SYS_CD_GROUP_BAS.SYS_GROUP_ID"), primary_key=True)
    SYS_CD_ID: Mapped[str] = mapped_column(String(50), primary_key=True)
    SYS_CD_NM: Mapped[str] = mapped_column(String(100), nullable=False)
    SYS_VAL: Mapped[str | None] = mapped_column(String(200), nullable=True)
    
    CRT_DT: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    UPD_DT: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    DESC_TXT: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    REF_VAL_1: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_2: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_3: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_4: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_5: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_6: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_7: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_8: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_9: Mapped[str | None] = mapped_column(String(200), nullable=True)
    REF_VAL_10: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Relationship back to SYS_CD_GROUP_BAS
    group: Mapped["SystemCodeGroup"] = relationship(
        "SystemCodeGroup", back_populates="system_codes",
        primaryjoin="SystemCodeGroup.SYS_GROUP_ID == foreign(SystemCode.SYS_GROUP_ID)"
    )
