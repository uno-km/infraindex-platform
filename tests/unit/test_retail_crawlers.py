import pytest
from apps.worker.providers.retail import RetailUniversalCrawler

@pytest.mark.asyncio
async def test_retail_universal_crawler_returns_normalized_data():
    crawler = RetailUniversalCrawler()
    
    # Act
    raw_data = await crawler.fetch_raw_data()
    parsed = crawler.parse_instances(raw_data)
    normalized = crawler.normalize_pricing(parsed)
    
    # Assert
    assert len(normalized) == 5
    
    # Check GPU from Danawa
    gpu1 = normalized[0]
    assert gpu1["platform"] == "danawa"
    assert gpu1["hardware_type"] == "gpu"
    assert gpu1["model_name"] == "RTX 4090"
    assert gpu1["currency"] == "KRW"
    assert "price" in gpu1
    
    # Check CPU from Danawa
    cpu1 = normalized[3]
    assert cpu1["platform"] == "danawa"
    assert cpu1["hardware_type"] == "cpu"
    assert cpu1["model_name"] == "Ryzen 9 7950X"
    
    # Check RAM from Naver
    ram1 = normalized[4]
    assert ram1["platform"] == "naver"
    assert ram1["hardware_type"] == "ram"
    assert ram1["capacity_gb"] == 32
