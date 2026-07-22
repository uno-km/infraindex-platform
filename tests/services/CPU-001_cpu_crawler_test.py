"""
CPU Crawler & Data Pipeline Unit Tests
"""

import pytest
from typing import Any

class TestCPUCrawlers:
    def test_korean_universal_cpu_mode(self):
        from apps.services.gpu.crawler_korean import KoreanUniversalCrawler
        # Instantiating with CPU hardware type
        c = KoreanUniversalCrawler("cloudv", hardware_type="cpu")
        assert c.hardware_type == "cpu"
        assert c.provider_slug == "cloudv"

    @pytest.mark.asyncio
    async def test_korean_crawler_cpu_returns_normalized_data(self):
        from apps.services.gpu.crawler_korean import KoreanUniversalCrawler
        crawler = KoreanUniversalCrawler("cloudv", hardware_type="cpu")
        result = await crawler.execute_pipeline()
        
        # CPU instances should exist for cloudv
        assert len(result) > 0
        assert all("cpu_model" in r for r in result)
        assert all("cores" in r for r in result)
        assert all("hardware_type" in r and r["hardware_type"] == "cpu" for r in result)

    @pytest.mark.asyncio
    async def test_korean_crawler_gpu_returns_normalized_data(self):
        from apps.services.gpu.crawler_korean import KoreanUniversalCrawler
        # Fallback to GPU if omitted
        crawler = KoreanUniversalCrawler("cloudv")
        result = await crawler.execute_pipeline()
        
        assert len(result) > 0
        assert all("gpu_model" in r for r in result)
        assert all("hardware_type" in r and r["hardware_type"] == "gpu" for r in result)

    @pytest.mark.asyncio
    async def test_vessl_crawler_empty_cpu(self):
        from apps.services.gpu.crawler_korean import VesslCrawler
        crawler = VesslCrawler(hardware_type="cpu")
        result = await crawler.execute_pipeline()
        # Vessl currently has no cpu_instances in KOREAN_SITES/VESSL_INSTANCES
        assert len(result) == 0

