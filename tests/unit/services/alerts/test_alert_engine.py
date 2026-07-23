import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from apps.services.alerts.alert_engine import AlertEngine
from apps.api.models.alerts import AlertRule
from uuid import uuid4

@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)

@pytest.mark.asyncio
async def test_check_retail_alerts_triggers(mock_db_session):
    # Setup
    engine = AlertEngine()
    rule = AlertRule(
        id=uuid4(),
        target="RTX 4090",
        alert_type="retail_price",
        price_threshold=2200000,
        is_active=True
    )
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [rule]
    mock_db_session.execute.return_value = mock_result
    
    # Test triggering (price is below threshold)
    triggered = await engine.check_retail_alerts(mock_db_session, "RTX 4090", 2100000, "http://link")
    
    assert len(triggered) == 1
    assert triggered[0].rule_id == rule.id
    assert "RTX 4090" in triggered[0].message

@pytest.mark.asyncio
async def test_check_retail_alerts_no_trigger(mock_db_session):
    # Setup
    engine = AlertEngine()
    rule = AlertRule(
        id=uuid4(),
        target="RTX 4090",
        alert_type="retail_price",
        price_threshold=2200000,
        is_active=True
    )
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [rule]
    mock_db_session.execute.return_value = mock_result
    
    # Test not triggering (price is above threshold)
    triggered = await engine.check_retail_alerts(mock_db_session, "RTX 4090", 2300000, "http://link")
    
    assert len(triggered) == 0

@pytest.mark.asyncio
async def test_check_news_alerts_triggers(mock_db_session):
    engine = AlertEngine()
    rule = AlertRule(
        id=uuid4(),
        target="HBM3E",
        alert_type="news_keyword",
        is_active=True
    )
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [rule]
    mock_db_session.execute.return_value = mock_result
    
    article_mock = AsyncMock()
    article_mock.title = "삼성전자, 새로운 HBM3E 메모리 발표"
    article_mock.url = "http://news"
    
    triggered = await engine.check_news_alerts(mock_db_session, article_mock)
    
    assert len(triggered) == 1
    assert triggered[0].rule_id == rule.id
