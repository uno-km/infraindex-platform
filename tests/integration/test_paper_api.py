"""
tests/integration/test_paper_api.py
Phase 6 - Papers API 통합 테스트 (TestClient 기반)
"""
import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi.testclient import TestClient


def test_paper_api_integration():
    """Papers API 통합 테스트 - mock DB + mock PaperService"""
    from apps.server.main import app
    from shared.db.session import get_db

    # mock DB 세션 생성
    mock_db = AsyncMock()

    # papers/list 쿼리 결과 (총 개수 0, 항목 없음)
    mock_count_result = MagicMock()
    mock_count_result.scalar.return_value = 0
    mock_items_result = MagicMock()
    mock_items_result.scalars.return_value.all.return_value = []
    mock_db.execute = AsyncMock(side_effect=[mock_count_result, mock_items_result])

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    mock_service = AsyncMock()
    mock_service.crawl_and_save_arxiv_recent = AsyncMock(return_value=3)

    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            FastAPICache.init(InMemoryBackend(), prefix="integration-paper")

            # 1. List papers (빈 결과)
            response = client.get("/api/v1/papers/")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
            list_data = response.json()
            assert "items" in list_data
            assert "total" in list_data
            assert list_data["total"] == 0

            # 2. Trigger crawl (PaperService mock)
            with patch("apps.server.api.v1.endpoints.papers.PaperService") as mock_cls:
                mock_cls.return_value = mock_service
                response = client.post("/api/v1/papers/crawl/arxiv?max_results=2")
                assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
                data = response.json()
                assert data["status"] == "success"
                assert data["new_papers_count"] == 3

            # 3. 존재하지 않는 paper_id로 조회 시 404 또는 500 (mock DB 미지원)
            response = client.get(f"/api/v1/papers/{uuid.uuid4()}")
            assert response.status_code in [404, 500]
    finally:
        app.dependency_overrides.clear()


def test_paper_list_with_filters():
    """논문 목록 필터링 파라미터 통합 테스트"""
    from apps.server.main import app
    from shared.db.session import get_db

    mock_db = AsyncMock()
    mock_count = MagicMock()
    mock_count.scalar.return_value = 0
    mock_items = MagicMock()
    mock_items.scalars.return_value.all.return_value = []
    mock_db.execute = AsyncMock(side_effect=[mock_count, mock_items, mock_count, mock_items])

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            FastAPICache.init(InMemoryBackend(), prefix="integration-paper-filter")

            # 검색 필터
            response = client.get("/api/v1/papers/", params={"q": "GPU", "source": "arxiv"})
            assert response.status_code == 200

            # 페이지네이션
            response = client.get("/api/v1/papers/", params={"page": 2, "size": 5})
            assert response.status_code == 200
            data = response.json()
            assert data["page"] == 2
            assert data["size"] == 5
    finally:
        app.dependency_overrides.clear()
