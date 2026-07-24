from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from apps.api.models.base import Base

class SysBatSchBas(Base):
    """
    배치 스케줄 마스터 테이블 (BAS)
    """
    __tablename__ = "SYS_BAT_SCH_BAS"

    bat_id = Column("BAT_ID", String(50), primary_key=True, index=True, comment="배치 마스터 ID")
    bat_nm = Column("BAT_NM", String(100), nullable=False, comment="배치 그룹명")
    run_hr = Column("RUN_HR", String(50), nullable=True, comment="실행 시간(시)")
    run_min = Column("RUN_MIN", String(50), nullable=True, comment="실행 시간(분)")
    run_sec = Column("RUN_SEC", String(50), nullable=True, comment="실행 시간(초)")
    use_yn = Column("USE_YN", String(1), default="Y", comment="사용 여부")
    
    # 여유 컬럼
    ref_val_1 = Column("REF_VAL_1", String(200), nullable=True, comment="참조값 1")
    ref_val_2 = Column("REF_VAL_2", String(200), nullable=True, comment="참조값 2")
    ref_val_3 = Column("REF_VAL_3", String(200), nullable=True, comment="참조값 3")
    last_run_dt = Column("LAST_RUN_DT", DateTime, nullable=True, comment="마지막 실행 일시")
    nxt_run_dt = Column("NXT_RUN_DT", DateTime, nullable=True, comment="다음 실행 예정 일시")
    err_msg = Column("ERR_MSG", Text, nullable=True, comment="에러 메시지")
    
    crt_dt = Column("CRT_DT", DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), comment="생성일시")
    upd_dt = Column("UPD_DT", DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None), comment="수정일시")

    # 관계 설정
    details = relationship("SysBatSchDtl", back_populates="master_schedule", cascade="all, delete-orphan")


class SysBatSchDtl(Base):
    """
    배치 스케줄 세부 잡 테이블 (DTL)
    """
    __tablename__ = "SYS_BAT_SCH_DTL"

    bat_id = Column("BAT_ID", String(50), ForeignKey("SYS_BAT_SCH_BAS.BAT_ID"), primary_key=True, comment="배치 마스터 ID")
    job_id = Column("JOB_ID", String(50), primary_key=True, comment="세부 잡 ID")
    job_nm = Column("JOB_NM", String(100), nullable=False, comment="세부 잡명")
    
    exec_typ = Column("EXEC_TYP", String(20), nullable=False, comment="실행 방식 (SCRIPT, API, PLAYWRIGHT 등)")
    exec_path = Column("EXEC_PATH", String(255), nullable=False, comment="실행 경로/URL")
    run_ord = Column("RUN_ORD", Integer, default=1, comment="실행 순서")
    use_yn = Column("USE_YN", String(1), default="Y", comment="사용 여부")
    
    # 여유 컬럼
    ref_val_1 = Column("REF_VAL_1", String(200), nullable=True, comment="파라미터/참조값 1")
    ref_val_2 = Column("REF_VAL_2", String(200), nullable=True, comment="파라미터/참조값 2")
    ref_val_3 = Column("REF_VAL_3", String(200), nullable=True, comment="파라미터/참조값 3")
    last_run_dt = Column("LAST_RUN_DT", DateTime, nullable=True, comment="마지막 실행 일시")
    err_msg = Column("ERR_MSG", Text, nullable=True, comment="에러 메시지")
    
    crt_dt = Column("CRT_DT", DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), comment="생성일시")
    upd_dt = Column("UPD_DT", DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None), comment="수정일시")

    # 관계 설정
    master_schedule = relationship("SysBatSchBas", back_populates="details")


class SysBatSchHist(Base):
    """
    배치 스케줄 실행 이력 테이블 (HIST)
    """
    __tablename__ = "SYS_BAT_SCH_HIST"

    seq = Column("SEQ", Integer, primary_key=True, autoincrement=True, comment="이력 일련번호")
    bat_id = Column("BAT_ID", String(50), nullable=False, index=True, comment="배치 마스터 ID")
    job_id = Column("JOB_ID", String(50), nullable=False, index=True, comment="세부 잡 ID")
    
    status = Column("STATUS", String(20), nullable=False, comment="실행 결과 (SUCCESS / FAIL)")
    start_dt = Column("START_DT", DateTime, nullable=False, comment="시작 일시")
    end_dt = Column("END_DT", DateTime, nullable=False, comment="종료 일시")
    err_msg = Column("ERR_MSG", Text, nullable=True, comment="에러 발생 시 전문(Traceback)")
    
    crt_dt = Column("CRT_DT", DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), comment="생성일시")
