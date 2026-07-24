import pytest
from fastapi.testclient import TestClient
from apps.server.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_insights_correlation_invalid_timeframe():
    response = client.get("/api/v1/insights/correlation?timeframe=invalid")
    assert response.status_code == 400
    assert "Unsupported timeframe" in response.json()["detail"]

@pytest.mark.asyncio
async def test_insights_correlation_structure(monkeypatch):
    # Mock get_db dependency
    from unittest.mock import AsyncMock, MagicMock
    
    mock_db = AsyncMock()
    mock_financial_result = MagicMock()
    # Return (symbol, close, timestamp)
    mock_financial_result.all.return_value = [
        ("NVDA", 130.0, "2023-01-01T00:00:00Z"),
        ("NVDA", 143.0, "2023-01-02T00:00:00Z"),
        ("AMD", 160.0, "2023-01-01T00:00:00Z"),
        ("AMD", 152.0, "2023-01-02T00:00:00Z"),
    ]
    
    mock_retail_result = MagicMock()
    # Return (model, price, timestamp)
    mock_retail_result.all.return_value = [
        ("RTX 4090", 2000.0, "2023-01-01T00:00:00Z"),
        ("RTX 4090", 2200.0, "2023-01-02T00:00:00Z"),
    ]
    
    # db.execute is called twice
    mock_db.execute.side_effect = [mock_financial_result, mock_retail_result]
    
    # We should override it properly
    from shared.db.session import get_db
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.get("/api/v1/insights/correlation?timeframe=1w")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3 # NVDA, AMD, RTX 4090
    
    nvda = next(item for item in data if item["asset"] == "NVDA")
    assert nvda["percentage_change"] == 10.0 # (143-130)/130
    
    amd = next(item for item in data if item["asset"] == "AMD")
    assert amd["percentage_change"] == -5.0 # (152-160)/160
    
    rtx = next(item for item in data if item["asset"] == "Retail RTX 4090")
    assert rtx["percentage_change"] == 10.0 # (2200-2000)/2000
    
    app.dependency_overrides.clear()
