import pytest
from apps.batch.services.financial.crawler import StockMarketCrawler, DramFuturesCrawler

@pytest.mark.asyncio
async def test_dram_futures_crawler():
    crawler = DramFuturesCrawler()
    raw = await crawler.fetch_raw_data()
    parsed = crawler.parse_instances(raw)
    normalized = crawler.normalize_pricing(parsed)
    
    assert len(normalized) == 1
    assert normalized[0]["symbol"] == "DRAM_8Gb_DDR4"
    assert normalized[0]["asset_type"] == "future"
    assert normalized[0]["currency"] == "USD"
    assert "close" in normalized[0]

@pytest.mark.asyncio
async def test_stock_market_crawler_structure():
    # We won't actually download from yfinance in the unit test to avoid network flakiness,
    # so we mock the fetch_raw_data to return a dummy dataframe structure.
    from unittest.mock import AsyncMock
    import pandas as pd
    
    crawler = StockMarketCrawler()
    
    # Create mock MultiIndex DataFrame similar to yf.download(group_by="ticker")
    # For a single day
    columns = pd.MultiIndex.from_tuples([
        ("NVDA", "Open"), ("NVDA", "High"), ("NVDA", "Low"), ("NVDA", "Close"), ("NVDA", "Volume"),
        ("AMD", "Open"), ("AMD", "High"), ("AMD", "Low"), ("AMD", "Close"), ("AMD", "Volume")
    ])
    data = [[130.0, 135.0, 129.0, 134.0, 1000000, 160.0, 162.0, 158.0, 161.0, 2000000]]
    df = pd.DataFrame(data, columns=columns)
    
    crawler.fetch_raw_data = AsyncMock(return_value=df)
    crawler.SYMBOLS = ["NVDA", "AMD"] # limit for test
    
    raw = await crawler.fetch_raw_data()
    parsed = crawler.parse_instances(raw)
    normalized = crawler.normalize_pricing(parsed)
    
    assert len(normalized) == 2
    
    nvda = next(item for item in normalized if item["symbol"] == "NVDA")
    assert nvda["asset_type"] == "stock"
    assert nvda["close"] == 134.0
    assert nvda["currency"] == "USD"
    
    amd = next(item for item in normalized if item["symbol"] == "AMD")
    assert amd["close"] == 161.0
