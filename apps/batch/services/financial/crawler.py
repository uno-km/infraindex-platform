import asyncio
import logging
from typing import Any, Dict, List
from datetime import datetime, timezone

from apps.batch.worker.providers.common.base import BaseProviderCrawler
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
    메모리 시장 지표 크롤러.
    DRAMeXchange 등 실시간 DRAM 선물 API가 유료이므로,
    메모리 관련 반도체 기업(SK하이닉스, Micron, Samsung) 주가 데이터를
    yfinance로 수집하여 메모리 시장 동향의 대리 지표로 활용합니다.
    """
    name = "dram_proxy"
    # 메모리 관련 대표 종목
    MEMORY_SYMBOLS = ["000660.KS", "MU", "005930.KS"]  # SK하이닉스, Micron, 삼성전자

    @property
    def provider_slug(self) -> str:
        return self.name

    async def fetch_raw_data(self) -> Any:
        loop = asyncio.get_event_loop()
        def download_data():
            try:
                return yf.download(self.MEMORY_SYMBOLS, period="5d", group_by="ticker", auto_adjust=True, progress=False)
            except Exception as e:
                logger.error(f"[dram_proxy] yfinance 다운로드 실패: {e}")
                return None

        return await loop.run_in_executor(None, download_data)

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        if raw_data is None or (hasattr(raw_data, 'empty') and raw_data.empty):
            return []

        label_map = {
            "000660.KS": "SK Hynix (KRX)",
            "MU": "Micron Technology (NASDAQ)",
            "005930.KS": "Samsung Electronics (KRX)",
        }
        parsed = []
        for symbol in self.MEMORY_SYMBOLS:
            try:
                if len(self.MEMORY_SYMBOLS) > 1:
                    ticker_data = raw_data[symbol]
                else:
                    ticker_data = raw_data
                if not ticker_data.empty:
                    latest = ticker_data.iloc[-1]
                    parsed.append({
                        "symbol": symbol,
                        "name": label_map.get(symbol, symbol),
                        "asset_type": "memory_proxy_stock",
                        "close": float(latest.get("Close", 0)),
                        "currency": "KRW" if symbol.endswith(".KS") else "USD",
                    })
            except Exception as e:
                logger.warning(f"[dram_proxy] {symbol} 파싱 실패: {e}")
        return parsed

    def parse_instances(self, raw_data: Any) -> List[Dict[str, Any]]:
        return self.parse_instances(raw_data)

    def normalize_pricing(self, parsed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return parsed_data

    def save(self, data: List[Dict[str, Any]]) -> None:
        logger.info(f"[dram_proxy] {len(data)} 건 메모리 프록시 주가 수집 완료.")

