import asyncio
import feedparser
import logging
from datetime import datetime, timezone
from dateutil import parser as date_parser
from typing import List, Dict, Any
import html
import re

from apps.worker.providers.common.playwright_base import BasePlaywrightCrawler

logger = logging.getLogger(__name__)

class GlobalNewsCrawler:
    """
    글로벌 뉴스 및 미디어(유튜브) 크롤러.
    RSS Feed를 메인으로 사용하고 필요시 Playwright 기반 접근 가능성을 엽니다.
    """
    
    def __init__(self):
        self.keywords = ["반도체", "Nvidia", "GPU 가격", "DRAM", "Semiconductor"]
        
        # Google News RSS for specific keywords (한국어 & 영어 뉴스 믹스)
        self.google_news_base = "https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
        
        # Bloomberg, Reuters 등 RSS 제공 여부에 따라 추가
        self.feeds = []
        for kw in self.keywords:
            self.feeds.append({
                "source": "Google News",
                "url": self.google_news_base.format(keyword=kw),
                "keyword": kw
            })
            
    def _clean_html(self, raw_html: str) -> str:
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return html.unescape(cleantext).strip()

    def fetch_rss_feed(self, feed_info: Dict[str, str]) -> List[Dict[str, Any]]:
        """단일 RSS 피드를 가져와서 파싱합니다."""
        results = []
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries:
                try:
                    # 날짜 파싱
                    published_at = datetime.now(timezone.utc)
                    if hasattr(entry, 'published'):
                        try:
                            published_at = date_parser.parse(entry.published)
                        except Exception:
                            pass

                    # 요약 정리
                    summary = ""
                    if hasattr(entry, 'summary'):
                        summary = self._clean_html(entry.summary)
                    
                    results.append({
                        "title": html.unescape(entry.title).strip(),
                        "url": entry.link,
                        "source": feed_info["source"],
                        "published_at": published_at,
                        "summary": summary[:2000] if summary else "",
                        "keywords": feed_info["keyword"]
                    })
                except Exception as e:
                    logger.warning(f"Error parsing news entry: {e}")
                    continue
        except Exception as e:
            logger.error(f"Error fetching RSS feed {feed_info['url']}: {e}")
            
        return results

    async def crawl(self) -> List[Dict[str, Any]]:
        """
        등록된 모든 미디어/뉴스 소스를 크롤링합니다.
        (현재 RSS 위주이며 비동기 래퍼 사용)
        """
        logger.info("Starting Global News Crawl...")
        
        all_news = []
        
        # RSS Feeds (CPU/IO Bound - asyncio.to_thread 활용)
        for feed_info in self.feeds:
            # RSS 가져오기는 requests를 내부적으로 사용하므로 블로킹 방지를 위해 to_thread 사용
            news_items = await asyncio.to_thread(self.fetch_rss_feed, feed_info)
            all_news.extend(news_items)
            
        # 중복 URL 제거 (가장 빠른 published_at 유지 등)
        unique_news = {}
        for item in all_news:
            if item["url"] not in unique_news:
                unique_news[item["url"]] = item
            else:
                # 같은 기사인데 다른 키워드에 걸린 경우 키워드 합치기
                existing_keywords = unique_news[item["url"]]["keywords"].split(",")
                if item["keywords"] not in existing_keywords:
                    unique_news[item["url"]]["keywords"] += f",{item['keywords']}"

        results = list(unique_news.values())
        logger.info(f"Global News Crawl finished. Extracted {len(results)} unique articles.")
        return results
