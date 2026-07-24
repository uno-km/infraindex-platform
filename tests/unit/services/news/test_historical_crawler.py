"""
tests/unit/services/news/test_historical_crawler.py
Phase 8 - HistoricalCrawler 유닛 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date


class TestHistoricalCrawler:
    """히스토리컬 뉴스 크롤러 유닛 테스트"""

    def test_import(self):
        """HistoricalCrawler 임포트 가능해야 한다"""
        from apps.services.news.crawler_historical import HistoricalCrawler
        assert HistoricalCrawler is not None

    def test_date_range_month_split(self):
        """date_range_months가 월 단위로 날짜 범위를 분리해야 한다"""
        from apps.services.news.crawler_historical import date_range_months
        ranges = list(date_range_months(date(2024, 1, 1), date(2024, 3, 31)))
        assert len(ranges) == 3
        assert ranges[0] == (date(2024, 1, 1), date(2024, 1, 31))
        assert ranges[1] == (date(2024, 2, 1), date(2024, 2, 29))
        assert ranges[2] == (date(2024, 3, 1), date(2024, 3, 31))

    def test_date_range_single_month(self):
        """단일 월 범위도 정상 처리해야 한다"""
        from apps.services.news.crawler_historical import date_range_months
        ranges = list(date_range_months(date(2024, 6, 1), date(2024, 6, 30)))
        assert len(ranges) == 1

    def test_date_range_cross_year(self):
        """연도를 넘어가는 범위도 처리해야 한다"""
        from apps.services.news.crawler_historical import date_range_months
        ranges = list(date_range_months(date(2023, 11, 1), date(2024, 2, 28)))
        assert len(ranges) == 4  # Nov, Dec, Jan, Feb

    @pytest.mark.asyncio
    async def test_fetch_arxiv_historical_returns_list(self):
        """fetch_arxiv_historical이 논문 목록을 반환해야 한다"""
        from apps.services.news.crawler_historical import HistoricalCrawler

        crawler = HistoricalCrawler()

        mock_papers = [
            {"external_id": "arxiv:2401.00001", "title": "GPU Memory Bandwidth Analysis", "published_at": date(2024, 1, 5)},
            {"external_id": "arxiv:2401.00002", "title": "HBM3 Performance Study", "published_at": date(2024, 1, 10)},
        ]

        with patch.object(crawler, "_fetch_arxiv_page", new_callable=AsyncMock, return_value=mock_papers):
            results = await crawler.fetch_arxiv_historical(
                from_date=date(2024, 1, 1),
                to_date=date(2024, 1, 31),
                max_results=10
            )

        assert isinstance(results, list)
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_fetch_sitemap_urls_returns_list(self):
        """fetch_sitemap_urls가 URL 목록을 반환해야 한다"""
        from apps.services.news.crawler_historical import HistoricalCrawler

        crawler = HistoricalCrawler()
        mock_sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/article-1</loc><lastmod>2024-01-15</lastmod></url>
  <url><loc>https://example.com/article-2</loc><lastmod>2024-01-20</lastmod></url>
</urlset>"""

        with patch.object(crawler, "_fetch_raw", new_callable=AsyncMock, return_value=mock_sitemap_xml):
            urls = await crawler.fetch_sitemap_urls("https://example.com/sitemap.xml")

        assert isinstance(urls, list)
        assert len(urls) == 2
        assert "https://example.com/article-1" in urls

    @pytest.mark.asyncio
    async def test_fetch_sitemap_with_date_filter(self):
        """날짜 필터링 적용 시 범위 내 URL만 반환해야 한다"""
        from apps.services.news.crawler_historical import HistoricalCrawler

        crawler = HistoricalCrawler()
        mock_sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/article-old</loc><lastmod>2023-12-01</lastmod></url>
  <url><loc>https://example.com/article-new</loc><lastmod>2024-01-15</lastmod></url>
</urlset>"""

        with patch.object(crawler, "_fetch_raw", new_callable=AsyncMock, return_value=mock_sitemap_xml):
            urls = await crawler.fetch_sitemap_urls(
                "https://example.com/sitemap.xml",
                from_date=date(2024, 1, 1),
                to_date=date(2024, 1, 31)
            )

        assert len(urls) == 1
        assert "article-new" in urls[0]

    @pytest.mark.asyncio
    async def test_fetch_arxiv_empty_on_error(self):
        """arXiv 에러 시 빈 리스트 반환해야 한다 (예외 없이)"""
        from apps.services.news.crawler_historical import HistoricalCrawler

        crawler = HistoricalCrawler()

        with patch.object(crawler, "_fetch_arxiv_page", new_callable=AsyncMock, side_effect=Exception("API 에러")):
            results = await crawler.fetch_arxiv_historical(
                from_date=date(2024, 1, 1),
                to_date=date(2024, 1, 31)
            )

        assert results == []

    @pytest.mark.asyncio
    async def test_fetch_sitemap_empty_on_error(self):
        """sitemap 에러 시 빈 리스트 반환해야 한다"""
        from apps.services.news.crawler_historical import HistoricalCrawler

        crawler = HistoricalCrawler()

        with patch.object(crawler, "_fetch_raw", new_callable=AsyncMock, side_effect=Exception("네트워크 에러")):
            urls = await crawler.fetch_sitemap_urls("https://example.com/sitemap.xml")

        assert urls == []

    def test_rate_limit_seconds_default(self):
        """기본 rate limit이 설정되어 있어야 한다"""
        from apps.services.news.crawler_historical import HistoricalCrawler
        c = HistoricalCrawler()
        assert c.rate_limit_seconds >= 1.0
