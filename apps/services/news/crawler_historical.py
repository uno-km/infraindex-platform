"""
apps/services/news/crawler_historical.py
Phase 8 - 히스토리컬 뉴스 백필 크롤러

지원 소스:
  1. arXiv API — date range 검색
  2. RSS Sitemap (sitemap.xml) — URL 목록 추출 + 날짜 필터
  3. Wayback Machine — 아카이브 조회 (선택적)
"""
import asyncio
import calendar
import logging
import re
from datetime import date, timedelta
from typing import Any, Dict, Generator, List, Optional, Tuple
from xml.etree import ElementTree

import httpx

logger = logging.getLogger(__name__)

# arXiv API base URL (공개 API, 인증 불필요)
ARXIV_API_URL = "https://export.arxiv.org/api/query"
# GPU/반도체 관련 arXiv 카테고리
ARXIV_CATEGORIES = ["cs.AR", "cs.DC", "cs.LG", "eess.SP"]
# GPU 관련 arXiv 검색어
ARXIV_QUERY = "ti:(GPU OR HBM OR DRAM OR semiconductor OR NVIDIA OR memory)"


def date_range_months(
    from_date: date,
    to_date: date,
) -> Generator[Tuple[date, date], None, None]:
    """
    from_date ~ to_date를 월 단위로 분리하는 제너레이터.

    yields: (month_start, month_end) 튜플
    """
    current = date(from_date.year, from_date.month, 1)
    end = date(to_date.year, to_date.month, 1)

    while current <= end:
        last_day = calendar.monthrange(current.year, current.month)[1]
        month_start = max(current, from_date)
        month_end = min(date(current.year, current.month, last_day), to_date)
        yield (month_start, month_end)

        # 다음 달
        if current.month == 12:
            current = date(current.year + 1, 1, 1)
        else:
            current = date(current.year, current.month + 1, 1)


class HistoricalCrawler:
    """
    히스토리컬 뉴스/논문 백필 크롤러.

    사용 예:
        crawler = HistoricalCrawler()
        papers = await crawler.fetch_arxiv_historical(date(2022,1,1), date(2024,12,31))
        urls = await crawler.fetch_sitemap_urls("https://news.example.com/sitemap.xml")
    """

    def __init__(self, rate_limit_seconds: float = 2.0):
        self.rate_limit_seconds = rate_limit_seconds
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=30.0)
        return self._client

    async def _fetch_raw(self, url: str, params: Optional[Dict] = None) -> str:
        """HTTP GET → 텍스트 반환"""
        client = await self._get_client()
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.text

    async def _fetch_arxiv_page(
        self,
        from_date: date,
        to_date: date,
        start: int = 0,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        arXiv API를 통해 특정 날짜 범위의 논문 조회.
        submittedDate:[YYYYMMDD0000+TO+YYYYMMDD2359] 형식 사용.
        """
        date_filter = (
            f"submittedDate:[{from_date.strftime('%Y%m%d')}0000 "
            f"TO {to_date.strftime('%Y%m%d')}2359]"
        )
        query = f"({ARXIV_QUERY}) AND {date_filter}"

        params = {
            "search_query": query,
            "start": start,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }

        raw = await self._fetch_raw(ARXIV_API_URL, params=params)
        return self._parse_arxiv_feed(raw)

    def _parse_arxiv_feed(self, xml_text: str) -> List[Dict[str, Any]]:
        """arXiv Atom feed XML 파싱"""
        results = []
        try:
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "arxiv": "http://arxiv.org/schemas/atom",
            }
            root = ElementTree.fromstring(xml_text)
            for entry in root.findall("atom:entry", ns):
                try:
                    raw_id = entry.find("atom:id", ns).text.split("/abs/")[-1].split("v")[0]
                    external_id = f"arxiv:{raw_id}"

                    title_el = entry.find("atom:title", ns)
                    title = title_el.text.strip().replace("\n", " ") if title_el is not None else ""

                    published_el = entry.find("atom:published", ns)
                    published_at = None
                    if published_el is not None:
                        try:
                            from datetime import datetime
                            published_at = datetime.strptime(
                                published_el.text[:10], "%Y-%m-%d"
                            ).date()
                        except ValueError:
                            pass

                    summary_el = entry.find("atom:summary", ns)
                    abstract = summary_el.text.strip().replace("\n", " ") if summary_el is not None else ""

                    authors = [
                        a.find("atom:name", ns).text
                        for a in entry.findall("atom:author", ns)
                        if a.find("atom:name", ns) is not None
                    ]

                    cats = [
                        t.get("term", "")
                        for t in entry.findall("atom:category", ns)
                    ]
                    primary_cat = cats[0] if cats else None

                    link_el = entry.find("atom:link[@rel='alternate']", ns)
                    article_url = link_el.get("href", "") if link_el is not None else ""

                    results.append({
                        "external_id": external_id,
                        "title": title,
                        "published_at": published_at,
                        "category": primary_cat,
                        "url": article_url,
                        "metadata_json": {
                            "abstract": abstract,
                            "authors": authors,
                            "categories": cats,
                            "url": article_url,
                        },
                    })
                except Exception as e:
                    logger.warning(f"[HistoricalCrawler] arXiv entry 파싱 실패: {e}")
        except Exception as e:
            logger.error(f"[HistoricalCrawler] arXiv feed 파싱 실패: {e}")
        return results

    async def fetch_arxiv_historical(
        self,
        from_date: date,
        to_date: date,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        arXiv에서 날짜 범위 내 GPU/반도체 관련 논문 전체 조회.
        Rate limiting 적용.
        """
        all_papers: List[Dict[str, Any]] = []
        try:
            for month_start, month_end in date_range_months(from_date, to_date):
                logger.info(f"[HistoricalCrawler] arXiv 조회: {month_start} ~ {month_end}")
                papers = await self._fetch_arxiv_page(
                    from_date=month_start,
                    to_date=month_end,
                    max_results=max_results,
                )
                all_papers.extend(papers)
                if len(list(date_range_months(from_date, to_date))) > 1:
                    await asyncio.sleep(self.rate_limit_seconds)
        except Exception as e:
            logger.error(f"[HistoricalCrawler] fetch_arxiv_historical 실패: {e}")
            return []

        logger.info(f"[HistoricalCrawler] arXiv 총 {len(all_papers)}건 수집 완료")
        return all_papers

    async def fetch_sitemap_urls(
        self,
        sitemap_url: str,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> List[str]:
        """
        sitemap.xml에서 URL 목록 추출.
        날짜 필터링 지원 (lastmod 기준).
        """
        try:
            raw = await self._fetch_raw(sitemap_url)
            return self._parse_sitemap(raw, from_date=from_date, to_date=to_date)
        except Exception as e:
            logger.error(f"[HistoricalCrawler] sitemap 조회 실패 ({sitemap_url}): {e}")
            return []

    def _parse_sitemap(
        self,
        xml_text: str,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    ) -> List[str]:
        """sitemap.xml XML 파싱 → URL 목록"""
        urls = []
        try:
            # namespace 제거 후 파싱
            xml_clean = re.sub(r'\s+xmlns[^"]*"[^"]*"', '', xml_text)
            root = ElementTree.fromstring(xml_clean)

            for url_el in root.findall(".//url"):
                loc_el = url_el.find("loc")
                if loc_el is None or not loc_el.text:
                    continue

                loc = loc_el.text.strip()

                # 날짜 필터링
                if from_date or to_date:
                    lastmod_el = url_el.find("lastmod")
                    if lastmod_el is not None and lastmod_el.text:
                        try:
                            lastmod = date.fromisoformat(lastmod_el.text[:10])
                            if from_date and lastmod < from_date:
                                continue
                            if to_date and lastmod > to_date:
                                continue
                        except ValueError:
                            pass  # 날짜 파싱 실패 시 포함

                urls.append(loc)
        except Exception as e:
            logger.error(f"[HistoricalCrawler] sitemap 파싱 실패: {e}")

        return urls

    async def fetch_wayback(
        self,
        url: str,
        timestamp: Optional[str] = None,
    ) -> Optional[str]:
        """
        Wayback Machine에서 특정 URL의 아카이브 조회.
        timestamp: YYYYMMDDHHMMSS 형식 (생략 시 가장 최근 스냅샷)
        반환: 아카이브 HTML 또는 None
        """
        try:
            check_url = f"https://archive.org/wayback/available?url={url}"
            if timestamp:
                check_url += f"&timestamp={timestamp}"

            raw = await self._fetch_raw(check_url)
            import json
            data = json.loads(raw)
            closest = data.get("archived_snapshots", {}).get("closest", {})

            if not closest.get("available"):
                return None

            archive_url = closest.get("url", "")
            if not archive_url:
                return None

            content = await self._fetch_raw(archive_url)
            return content

        except Exception as e:
            logger.warning(f"[HistoricalCrawler] Wayback Machine 조회 실패 ({url}): {e}")
            return None

    async def close(self):
        """HTTP 클라이언트 닫기"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
