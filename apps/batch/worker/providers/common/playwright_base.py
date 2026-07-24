import logging
from abc import abstractmethod
from typing import Any
from playwright.async_api import async_playwright
from apps.batch.worker.providers.common.base import BaseProviderCrawler

class BasePlaywrightCrawler(BaseProviderCrawler):
    """
    Extends BaseProviderCrawler to use Playwright for headless browser scraping.
    Useful for SPA sites (Vue.js, React) or sites that block simple HTTP requests.
    """
    
    async def fetch_raw_data_via_browser(self, url: str) -> str:
        """
        Launches Playwright, navigates to the URL, and returns the fully rendered HTML.
        Can be overridden for more complex interactions (clicking, waiting for elements).
        """
        self.logger.info(f"[{self.provider_slug}] Launching Playwright to scrape {url}")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            try:
                await page.goto(url, wait_until="networkidle", timeout=60000)
                # Let's wait a bit extra for dynamic frameworks to settle
                await page.wait_for_timeout(3000)
                html = await page.content()
                return html
            except Exception as e:
                self.logger.error(f"[{self.provider_slug}] Playwright error: {e}")
                return ""
            finally:
                await browser.close()
