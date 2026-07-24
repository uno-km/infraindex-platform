import random
import httpx
from typing import Optional, List
from apps.batch.worker.core.config import settings

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
]

class ProxyManager:
    """
    Enterprise-grade Proxy Rotation Manager (Anti-Bot).
    """
    def __init__(self, proxy_list: Optional[List[str]] = None):
        self.proxies = proxy_list or []
        self.current_index = 0

    def get_next_proxy(self) -> Optional[str]:
        if not self.proxies or not settings.USE_PROXY:
            return None
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy

class StealthHttpClient:
    """
    HTTP Client with User-Agent spoofing and feature-flagged Proxy support.
    """
    def __init__(self, proxy_manager: Optional[ProxyManager] = None):
        self.proxy_manager = proxy_manager or ProxyManager()

    def _get_random_headers(self) -> dict:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    async def get_client(self) -> httpx.AsyncClient:
        headers = self._get_random_headers()
        proxy_url = self.proxy_manager.get_next_proxy()
        
        # httpx >= 0.27 uses `proxy` or `proxies` kwarg.
        kwargs = {"headers": headers, "timeout": 30.0}
        if proxy_url:
            kwargs["proxy"] = proxy_url
            
        return httpx.AsyncClient(**kwargs)
