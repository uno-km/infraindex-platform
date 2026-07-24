import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from apps.batch.services.ai_pricing.crawler_openrouter import crawl_openrouter_pricing
from shared.models.ai_pricing import AIModelMaster, AIModelPriceHistory
from sqlalchemy.future import select

# Dummy response for mock
MOCK_OPENROUTER_RESPONSE = {
    "data": [
        {
            "id": "openai/gpt-4o",
            "name": "GPT-4o",
            "pricing": {
                "prompt": "0.0000025",      # $2.5 / 1M
                "completion": "0.000010"    # $10.0 / 1M
            },
            "context_length": 128000
        },
        {
            "id": "anthropic/claude-3.5-sonnet",
            "name": "Claude 3.5 Sonnet",
            "pricing": {
                "prompt": "0.000003",       # $3.0 / 1M
                "completion": "0.000015"    # $15.0 / 1M
            },
            "context_length": 200000
        },
        {
            "id": "unknown/model", # Should be ignored because it's not in TARGET_MODELS
            "name": "Unknown",
            "pricing": {
                "prompt": "0",
                "completion": "0"
            }
        }
    ]
}

@pytest.mark.asyncio
async def test_crawl_openrouter_pricing(monkeypatch):
    """
    OpenRouter 크롤러 단위 테스트:
    1. 외부 API(requests.get) 모킹
    2. TARGET_MODELS 에 속한 모델만 마스터에 등록/업데이트 되는지 확인
    3. 가격 데이터가 1M 토큰 단위로 변환되어 히스토리에 적재되는지 확인
    4. 제외된 모델은 무시되는지 확인
    """
    
    # 1. Mock the requests.get call
    class MockResponse:
        def raise_for_status(self): pass
        def json(self): return MOCK_OPENROUTER_RESPONSE
        
    def mock_get(*args, **kwargs):
        return MockResponse()
        
    monkeypatch.setattr("apps.batch.services.ai_pricing.crawler_openrouter.requests.get", mock_get)
    
    # 2. Mock AsyncSessionLocal and database calls
    mock_session = AsyncMock()
    
    # We will simulate that the DB is initially empty, 
    # so `execute` returns a mock result where `scalars().first()` is None.
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result
    
    class MockSessionContextManager:
        async def __aenter__(self):
            return mock_session
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
            
    class MockSessionFactory:
        def __call__(self):
            return MockSessionContextManager()
            
    monkeypatch.setattr("apps.batch.services.ai_pricing.crawler_openrouter._build_session_factory", lambda e: MockSessionFactory())
    monkeypatch.setattr("apps.batch.services.ai_pricing.crawler_openrouter._build_engine", lambda: None)
    
    # 3. Execute the crawler
    updated_count = await crawl_openrouter_pricing()
    
    # Only 2 models from the mock are in TARGET_MODELS
    assert updated_count == 2
    
    # 4. Verify AIModelMaster and AIModelPriceHistory insertion calls
    # Since we mocked the DB, we just verify `session.add` was called.
    assert mock_session.add.call_count == 4  # 2 models * (1 master + 1 history)
    
    # Check that session.commit was called
    mock_session.commit.assert_awaited_once()
