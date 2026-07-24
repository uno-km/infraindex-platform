"""
Task ID: 92b9d69c-1bb1-4616-ae49-9bd85dcd002b
TDD Test Suite for User Refinement (user_bas, user_fvrt, user_stng)
"""
import pytest
import pytest_asyncio
import uuid
from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient

# Mocking database dependencies
@pytest.fixture
def mock_db():
    db = AsyncMock()
    return db

@pytest_asyncio.fixture
async def async_api_client():
    from apps.server.main import app
    from shared.db.session import get_db
    from apps.server.api.deps import get_current_user
    from shared.models.user import UserBas
    from httpx import ASGITransport, AsyncClient
    
    # Create mock user
    mock_user = UserBas(
        id=uuid.uuid4(),
        email="admin@test.com",
        nickname="admin",
        is_admin=True,
        oauth_provider=None
    )
    
    async def override_get_current_user():
        return mock_user
        
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
        
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_read_user_me(async_api_client):
    """
    Test GET /api/v1/users/me
    """
    response = await async_api_client.get("/api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@test.com"
    assert data["nickname"] == "admin"
    assert data["is_admin"] is True


@pytest.mark.asyncio
async def test_add_favorite_mocked(async_api_client):
    """
    Test POST /api/v1/users/favorites (mocked DB response in route or simply checking validation)
    Note: Since we overrode get_current_user, we would need to override get_db to fully mock DB logic 
    if we don't want to hit real DB. For now, testing the schema rejection if invalid.
    """
    response = await async_api_client.post("/api/v1/users/favorites", json={
        # missing target_id and target_type
    })
    assert response.status_code == 422 # Validation Error
    
    # This requires DB hit in real implementation, so we only test validation layer here 
    # unless we fully mock get_db in the fixture.
