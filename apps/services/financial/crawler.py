import asyncio
import logging
from typing import Any, Dict, List
from datetime import datetime, timezone

from apps.worker.providers.common.base import BaseProviderCrawler
import yfinance as yf

logger = logging.getLogger(__name__)

class StockMarketCrawler(BaseProviderCrawler):
    """
    Crawler to fetch official stock market prices via Yahoo Finance.
    """
    name = "stock_market"
    
    # Symbols of interest (NVDA, AMD, Samsung Electronics, SK Hynix, Western Digital)
    SYMBOLS = ["NVDA", "AMD", "005930.KS", "000660.KS", "WDC"]

    @property
    def provider_slug(self) -> str:
        return self.name

    async def fetch_raw_data(self) -> Any:
        """
        Uses yfinance to fetch live/latest stock data for all target symbols.
        Running this async as downloading multiple tickers can take a few seconds.
        """
        # Run in executor because yfinance is synchronous
        loop = asyncio.get_event_loop()
        def download_data():
            try:
                # download past 5 days to ensure we get a valid latest close
                return yf.download(self.SYMBOLS, period="5d", group_by="ticker", auto_adjust=True, progress=False)
            except Exception as e:
                logger.error(f"Error downloading yfinance data: {e}")
                return None
                
        return await loop.run_in_executor(None, download_data)

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        """
        Extracts the latest close price for each symbol from the yfinance DataFrame.
        """
        if raw_data is None or raw_data.empty:
            return []
            
        parsed = []
        for symbol in self.SYMBOLS:
            try:
                # If multiple tickers are downloaded, columns are a MultiIndex
                if len(self.SYMBOLS) > 1:
                    ticker_data = raw_data[symbol]
                else:
                    ticker_data = raw_data
                    
                if not ticker_data.empty:
                    # Get the most recent row
                    latest = ticker_data.iloc[-1]
                    
                    parsed.append({
                        "symbol": symbol,
                        "asset_type": "stock",
                        "open": float(latest.get("Open", 0)),
                        "high": float(latest.get("High", 0)),
                        "low": float(latest.get("Low", 0)),
                        "close": float(latest.get("Close", 0)),
                        "volume": float(latest.get("Volume", 0)),
                        "currency": "KRW" if symbol.endswith(".KS") else "USD"
                    })
            except Exception as e:
                logger.error(f"Failed to parse data for {symbol}: {e}")
                
        return parsed

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # For stocks, parsing already standardizes it.
        return parsed_data
        
    def save(self, data: List[Dict[str, Any]]) -> None:
        """
        Saves the normalized data into FinMktHistory.
        """
        print(f"[StockMarketCrawler] Ready to save {len(data)} stock market records.")


class DramFuturesCrawler(BaseProviderCrawler):
    """
    Mock crawler for DRAM Futures. Real APIs are often paywalled (e.g. DRAMeXchange).
    This simulates futures volatility tracking.
    """
    name = "dram_futures"

    @property
    def provider_slug(self) -> str:
        return self.name

    async def fetch_raw_data(self) -> Any:
        import random
        await asyncio.sleep(0.1)
        base_price = 2.50 # Base price for 8Gb DDR4
        volatility = random.uniform(0.95, 1.05)
        
        return {
            "symbol": "DRAM_8Gb_DDR4",
            "asset_type": "future",
            "open": base_price,
            "high": base_price * 1.02,
            "low": base_price * 0.98,
            "close": base_price * volatility,
            "volume": random.randint(1000, 50000),
            "currency": "USD"
        }

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        return [raw_data]

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return parsed_data
        
    def save(self, data: List[Dict[str, Any]]) -> None:
        print(f"[DramFuturesCrawler] Ready to save {len(data)} futures market records.")
