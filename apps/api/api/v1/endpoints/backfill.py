"""
apps/api/api/v1/endpoints/backfill.py
Phase 8 - 히스토리컬 뉴스 백필 API 엔드포인트

Routes:
  POST /api/v1/backfill/news          — 날짜 범위 백필 시작
  GET  /api/v1/backfill/status        — 모든 백필 작업 목록
  GET  /api/v1/backfill/status/{id}   — 특정 작업 상태 조회
  POST /api/v1/backfill/{id}/cancel   — 작업 취소
"""
import logging
import uuid
from datetime import date, datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.core.database import get_db
from apps.api.models.backfill import BackfillJob

logger = logging.getLogger(__name__)
router = APIRouter()


# ─────────────────────────── Pydantic Schemas ────────────────────────────────

class BackfillRequest(BaseModel):
    source: str = Field(default="arxiv", description="백필 소스 (arxiv / sitemap / all)")
    from_date: date = Field(..., description="시작 날짜 (YYYY-MM-DD)")
    to_date: date = Field(..., description="종료 날짜 (YYYY-MM-DD)")
    max_results_per_month: int = Field(default=100, ge=1, le=500, description="월별 최대 수집 건수")

    class Config:
        json_schema_extra = {
            "example": {
                "source": "arxiv",
                "from_date": "2023-01-01",
                "to_date": "2023-12-31",
                "max_results_per_month": 100,
            }
        }


class BackfillJobResponse(BaseModel):
    id: str
    source: str
    from_date: date
    to_date: date
    status: str
    total_urls: int
    processed: int
    new_articles: int
    progress_pct: Optional[float]
    duration_seconds: Optional[float]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    error_msg: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ─────────────────────────── Background Task ─────────────────────────────────

async def _run_backfill(job_id: str, request: BackfillRequest, db_factory):
    """
    백그라운드에서 실행되는 백필 작업.
    DB 세션을 독립적으로 사용.
    """
    from apps.services.news.crawler_historical import HistoricalCrawler
    from apps.services.news.duplicate_detector import DuplicateDetector

    crawler = HistoricalCrawler(rate_limit_seconds=2.0)
    detector = DuplicateDetector(similarity_threshold=0.85)

    async with db_factory() as db:
        # Job 상태 → running
        result = await db.execute(select(BackfillJob).where(BackfillJob.id == job_id))
        job = result.scalars().first()
        if not job:
            return

        job.status = "running"
        job.started_at = datetime.now(timezone.utc)
        await db.commit()

        new_count = 0
        processed = 0

        try:
            if request.source in ("arxiv", "all"):
                papers = await crawler.fetch_arxiv_historical(
                    from_date=request.from_date,
                    to_date=request.to_date,
                    max_results=request.max_results_per_month,
                )
                job.total_urls = len(papers)
                await db.commit()

                for paper in papers:
                    article_dict = {
                        "url": paper.get("url", ""),
                        "title": paper.get("title", ""),
                    }
                    processed += 1
                    if not detector.is_duplicate(article_dict):
                        detector.register_article(article_dict)
                        new_count += 1

                    job.processed = processed
                    job.new_articles = new_count
                    if processed % 20 == 0:
                        await db.commit()

            # 완료 처리
            job.status = "done"
            job.finished_at = datetime.now(timezone.utc)
            job.processed = processed
            job.new_articles = new_count
            await db.commit()
            logger.info(f"[Backfill] Job {job_id} 완료: {new_count}건 신규")

        except Exception as e:
            logger.error(f"[Backfill] Job {job_id} 실패: {e}")
            job.status = "failed"
            job.error_msg = str(e)
            job.finished_at = datetime.now(timezone.utc)
            await db.commit()
        finally:
            await crawler.close()


# ─────────────────────────── API Endpoints ───────────────────────────────────

@router.post("/news", response_model=BackfillJobResponse, status_code=202)
async def start_backfill(
    request: BackfillRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    히스토리컬 뉴스 백필 작업 시작.
    즉시 job_id를 반환하고 백그라운드에서 수집을 진행합니다.
    """
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    if request.from_date > request.to_date:
        raise HTTPException(status_code=400, detail="from_date must be before to_date")

    # 날짜 범위 제한 (최대 3년)
    delta = (request.to_date - request.from_date).days
    if delta > 365 * 3:
        raise HTTPException(
            status_code=400,
            detail="Date range cannot exceed 3 years. Please split into smaller ranges."
        )

    # BackfillJob 생성
    job = BackfillJob(
        source=request.source,
        from_date=request.from_date,
        to_date=request.to_date,
        status="pending",
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    # 백그라운드 태스크 등록
    from apps.api.core.database import AsyncSessionLocal
    background_tasks.add_task(_run_backfill, str(job.id), request, AsyncSessionLocal)

    logger.info(f"[Backfill] Job {job.id} 생성: {request.source} {request.from_date}~{request.to_date}")
    return _job_to_response(job)


@router.get("/status", response_model=List[BackfillJobResponse])
async def list_backfill_jobs(
    source: Optional[str] = Query(None, description="소스 필터"),
    status: Optional[str] = Query(None, description="상태 필터 (pending/running/done/failed)"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """백필 작업 목록 조회"""
    if db is None:
        return []

    stmt = select(BackfillJob).order_by(desc(BackfillJob.created_at)).limit(limit)
    if source:
        stmt = stmt.where(BackfillJob.source == source)
    if status:
        stmt = stmt.where(BackfillJob.status == status)

    result = await db.execute(stmt)
    jobs = result.scalars().all()
    return [_job_to_response(j) for j in jobs]


@router.get("/status/{job_id}", response_model=BackfillJobResponse)
async def get_backfill_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
):
    """특정 백필 작업 상태 조회"""
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    try:
        uuid.UUID(job_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid job_id format")

    result = await db.execute(select(BackfillJob).where(BackfillJob.id == job_id))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Backfill job {job_id} not found")

    return _job_to_response(job)


@router.post("/{job_id}/cancel")
async def cancel_backfill_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
):
    """실행 중인 백필 작업 취소 (pending/running 상태만 가능)"""
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    result = await db.execute(select(BackfillJob).where(BackfillJob.id == job_id))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    if job.status not in ("pending", "running"):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job in '{job.status}' status"
        )

    job.status = "cancelled"
    job.finished_at = datetime.now(timezone.utc)
    await db.commit()

    return {"message": f"Job {job_id} cancelled", "status": "cancelled"}


# ─────────────────────────── Helper ──────────────────────────────────────────

def _job_to_response(job: BackfillJob) -> BackfillJobResponse:
    return BackfillJobResponse(
        id=str(job.id),
        source=job.source,
        from_date=job.from_date,
        to_date=job.to_date,
        status=job.status,
        total_urls=job.total_urls or 0,
        processed=job.processed or 0,
        new_articles=job.new_articles or 0,
        progress_pct=job.progress_pct,
        duration_seconds=job.duration_seconds,
        started_at=job.started_at,
        finished_at=job.finished_at,
        error_msg=job.error_msg,
        created_at=job.created_at,
    )
