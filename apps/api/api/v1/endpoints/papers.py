from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List, Dict, Any
from datetime import date

from apps.api.core.database import get_db
from apps.api.models.paper import PaperArticle
from apps.services.paper.paper_service import PaperService

router = APIRouter()

@router.get("/", summary="Get list of papers")
async def list_papers(
    q: Optional[str] = Query(None, description="Search query in title"),
    source: Optional[str] = Query(None, description="Filter by source e.g., arxiv"),
    category: Optional[str] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    if db is None:
        return {"items": [], "total": 0, "page": page, "size": size}
        
    stmt = select(PaperArticle)
    
    if q:
        stmt = stmt.where(PaperArticle.title.ilike(f"%{q}%"))
    if source:
        stmt = stmt.where(PaperArticle.source == source)
    if category:
        stmt = stmt.where(PaperArticle.category == category)
        
    # Count total
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0
    
    # Paginate
    stmt = stmt.order_by(PaperArticle.published_at.desc(), PaperArticle.created_at.desc())
    stmt = stmt.offset((page - 1) * size).limit(size)
    
    result = await db.execute(stmt)
    papers = result.scalars().all()
    
    items = []
    for p in papers:
        items.append({
            "id": p.id,
            "external_id": p.external_id,
            "source": p.source,
            "title": p.title,
            "title_ko": p.title_ko,
            "published_at": p.published_at,
            "category": p.category,
            "citation_count": p.citation_count,
            "is_analyzed": p.is_analyzed,
            "metadata": p.metadata_json
        })
        
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size
    }

@router.get("/{paper_id}", summary="Get paper details")
async def get_paper(paper_id: str, db: AsyncSession = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=404, detail="DB not available")
        
    stmt = select(PaperArticle).where(PaperArticle.id == paper_id)
    result = await db.execute(stmt)
    p = result.scalars().first()
    
    if not p:
        raise HTTPException(status_code=404, detail="Paper not found")
        
    return {
        "id": p.id,
        "external_id": p.external_id,
        "source": p.source,
        "title": p.title,
        "title_ko": p.title_ko,
        "published_at": p.published_at,
        "category": p.category,
        "citation_count": p.citation_count,
        "is_analyzed": p.is_analyzed,
        "metadata": p.metadata_json,
        "created_at": p.crawled_at
    }

@router.post("/crawl/arxiv", summary="Trigger ArXiv manual crawl")
async def trigger_crawl_arxiv(
    max_results: int = Query(10, description="Max results to fetch"),
    db: AsyncSession = Depends(get_db)
):
    if db is None:
        raise HTTPException(status_code=400, detail="Database not available")
        
    service = PaperService(db)
    try:
        new_count = await service.crawl_and_save_arxiv_recent(max_results=max_results)
        return {"status": "success", "new_papers_count": new_count}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Crawl failed: {repr(e)}")
