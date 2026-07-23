import pytest
from unittest.mock import patch, MagicMock
from apps.services.market.crawler_coupang import CoupangCrawler

@pytest.fixture
def mock_coupang_crawler():
    crawler = CoupangCrawler()
    crawler.access_key = "test_access"
    crawler.secret_key = "test_secret"
    return crawler

def test_generate_hmac(mock_coupang_crawler):
    hmac_header = mock_coupang_crawler._generate_hmac("GET", "/test/path", "keyword=RTX")
    assert "CEA algorithm=HmacSHA256" in hmac_header
    assert "access-key=test_access" in hmac_header
    assert "signature=" in hmac_header

@patch("apps.services.market.crawler_coupang.urllib.request.urlopen")
def test_search_products_success(mock_urlopen, mock_coupang_crawler):
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"rCode": "0", "data": {"productData": [{"productName": "RTX 4090", "productPrice": 3000000}]}}'
    mock_urlopen.return_value.__enter__.return_value = mock_response

    results = mock_coupang_crawler.search_products("RTX 4090")
    
    assert len(results) == 1
    assert results[0]["productName"] == "RTX 4090"
    assert results[0]["productPrice"] == 3000000

@patch("apps.services.market.crawler_coupang.urllib.request.urlopen")
def test_search_products_error(mock_urlopen, mock_coupang_crawler):
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"rCode": "401", "rMessage": "Unauthorized"}'
    mock_urlopen.return_value.__enter__.return_value = mock_response

    results = mock_coupang_crawler.search_products("RTX 4090")
    
    assert len(results) == 0

@patch("apps.services.market.crawler_coupang.urllib.request.urlopen")
def test_search_products_filters_accessories(mock_urlopen, mock_coupang_crawler):
    mock_response = MagicMock()
    # "팬", "쿨러" 등의 금지어가 포함된 데이터와 정상 데이터를 함께 반환
    mock_response.read.return_value = '{"rCode": "0", "data": {"productData": [{"productName": "RTX 4090", "productPrice": 3000000}, {"productName": "RTX 4090 쿨러 팬", "productPrice": 50000}]}}'.encode('utf-8')
    mock_urlopen.return_value.__enter__.return_value = mock_response

    results = mock_coupang_crawler.search_products("RTX 4090")
    
    # 쿨러가 필터링되어 1개만 남아야 함
    assert len(results) == 1
    assert results[0]["productName"] == "RTX 4090"
