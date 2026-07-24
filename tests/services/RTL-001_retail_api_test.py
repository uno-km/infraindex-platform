import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timezone

# We'll mock the database so we don't need a real Postgres connection
from unittest.mock import patch, MagicMock, AsyncMock

@pytest.fixture
def mock_db_result():
    # Mocking the result of the text(stmt) query
    mock_result = MagicMock()
    
    class MockRow:
        def __init__(self, t, o, h, l, c):
            self.time = t
            self.open = o
            self.high = h
            self.low = l
            self.close = c
    
    mock_result.fetchall.return_value = [
        MockRow(datetime(2023, 1, 1, 10, 0, tzinfo=timezone.utc), 1000, 1200, 900, 1100),
        MockRow(datetime(2023, 1, 1, 11, 0, tzinfo=timezone.utc), 1100, 1300, 1000, 1250),
    ]
    return mock_result

@pytest.mark.asyncio
async def test_retail_ohlc_returns_correct_structure(mock_db_result):
    from apps.server.main import app
    from shared.config.settings import settings
    from shared.db.session import get_db
    
    # Bypass the database dependency
    settings.USE_REAL_DB = False
    
    # Mock AsyncSession
    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_db_result
    
    async def override_get_db():
        yield mock_session
        
    app.dependency_overrides[get_db] = override_get_db
    
    # Mock the rate limiter so tests pass
    def mock_check_limit(*args, **kwargs):
        for arg in args:
            if hasattr(arg, "state"):
                arg.state.view_rate_limit = []
                break

    with patch("slowapi.extension.Limiter._check_request_limit", side_effect=mock_check_limit):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.get("/api/v1/retail/ohlc?hardware_type=gpu&model_name=RTX 4090&timeframe=1h")
            
            assert response.status_code == 200
            data = response.json()
            
            assert len(data) == 2
            assert data[0]["open"] == 1000
            assert data[0]["high"] == 1200
            assert data[0]["low"] == 900
            assert data[0]["close"] == 1100
            assert "time" in data[0]

@pytest.mark.asyncio
async def test_retail_ohlc_invalid_timeframe():
    from apps.server.main import app
    
    def mock_check_limit(*args, **kwargs):
        for arg in args:
            if hasattr(arg, "state"):
                arg.state.view_rate_limit = []
                break

    with patch("slowapi.extension.Limiter._check_request_limit", side_effect=mock_check_limit):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.get("/api/v1/retail/ohlc?hardware_type=gpu&model_name=RTX 4090&timeframe=invalid")
            
            assert response.status_code == 400
            assert "Invalid timeframe" in response.json()["detail"]
