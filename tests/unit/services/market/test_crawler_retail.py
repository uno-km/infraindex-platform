import pytest
from unittest.mock import patch, MagicMock
from apps.services.market.crawler_retail import RetailCrawler

@pytest.fixture
def mock_retail_crawler():
    return RetailCrawler()

@pytest.mark.asyncio
@patch("apps.services.market.crawler_retail.urllib.request.urlopen")
async def test_retail_search_products_success(mock_urlopen, mock_retail_crawler):
    # Mock response
    mock_response = MagicMock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'{"items": [{"title": "RTX 4090", "lprice": "3000000", "mallName": "Naver", "link": "http"}]}'
    mock_urlopen.return_value = mock_response

    results = await mock_retail_crawler.search_naver_shopping("RTX 4090")
    
    assert len(results) == 1
    assert results[0]["title"] == "RTX 4090"
    assert results[0]["lprice"] == "3000000"

@pytest.mark.asyncio
@patch("apps.services.market.crawler_retail.urllib.request.urlopen")
async def test_retail_search_products_error(mock_urlopen, mock_retail_crawler):
    # Setup error
    mock_urlopen.side_effect = Exception("API Error")

    results = await mock_retail_crawler.search_naver_shopping("RTX 4090")
    
    assert len(results) == 0
