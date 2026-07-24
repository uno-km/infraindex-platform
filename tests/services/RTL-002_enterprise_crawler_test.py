import pytest
from httpx import AsyncClient, ASGITransport
from apps.server.main import app
from shared.db.session import get_db
from datetime import datetime, timezone
import json

@pytest.mark.asyncio
async def test_enterprise_crawler_structure(monkeypatch):
    from apps.batch.services.retail.crawler_enterprise import EnterpriseHardwareCrawler
    
    crawler = EnterpriseHardwareCrawler()
    
    # 1. Test extraction
    raw_prices = await crawler.fetch_raw_data()
    assert len(raw_prices) > 0
    
    # 2. Test standardization
    parsed = crawler.parse_instances(raw_prices)
    std_prices = crawler.normalize_pricing(parsed)
    assert len(std_prices) > 0
    assert std_prices[0]["hardware_type"] == "enterprise_gpu"
    assert "price" in std_prices[0]
    
@pytest.mark.asyncio
async def test_enterprise_api_structure(monkeypatch):
    from unittest.mock import AsyncMock, MagicMock

    mock_db = AsyncMock()
    mock_result = MagicMock()
    
    # model_name, platform, price, capacity_gb, product_url, is_official, timestamp
    mock_result.fetchall.return_value = [
        MagicMock(
            model_name="NVIDIA H100 80GB PCIe",
            platform="CDW",
            price=30000.0,
            capacity_gb=80.0,
            product_url="http://cdw.example",
            is_official=False,
            timestamp=datetime.now(timezone.utc)
        ),
        MagicMock(
            model_name="NVIDIA DGX H100 Server",
            platform="Official",
            price=480000.0,
            capacity_gb=640.0,
            product_url="http://nvidia.example",
            is_official=True,
            timestamp=datetime.now(timezone.utc)
        )
    ]
    mock_db.execute.return_value = mock_result

    app.dependency_overrides[get_db] = lambda: mock_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/retail/enterprise")
        
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["model_name"] == "NVIDIA H100 80GB PCIe"
    assert data[1]["price"] == 480000.0
    assert data[1]["is_official"] is True

    app.dependency_overrides.clear()
