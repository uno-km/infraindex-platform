"""
tests/e2e/test_community_e2e.py
Phase 10 (미구현) - 커뮤니티 게시판 API E2E 테스트
"""
import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


class TestCommunityE2E:

    @pytest.fixture
    def app_client(self):
        from fastapi.testclient import TestClient
        from apps.server.main import app
        from shared.db.session import get_db

        async def override_get_db():
            yield None

        app.dependency_overrides[get_db] = override_get_db

        with TestClient(app, raise_server_exceptions=False) as client:
            FastAPICache.init(InMemoryBackend(), prefix="e2e-community")
            yield client

        app.dependency_overrides.clear()

    def test_community_boards_404_or_200(self, app_client):
        """[미구현] 404(미구현) 또는 200(구현됨) 반환"""
        response = app_client.get("/api/v1/community/boards")
        assert response.status_code in [200, 404]

    def test_community_posts_404_or_200(self, app_client):
        """[미구현] 404(미구현) 또는 200(구현됨) 반환"""
        response = app_client.get("/api/v1/community/posts")
        assert response.status_code in [200, 404]

    def test_community_post_create_not_500(self, app_client):
        """[미구현] 500을 반환하지 않아야 한다"""
        response = app_client.post(
            "/api/v1/community/posts",
            json={"board_id": "test", "title": "Test", "content": "Test"}
        )
        assert response.status_code != 500

    @pytest.mark.xfail(reason="Community feature not yet implemented (Phase 10)")
    def test_community_returns_200_after_impl(self, app_client):
        """구현 후 200 반환 (현재 xfail)"""
        response = app_client.get("/api/v1/community/boards")
        assert response.status_code == 200
