import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime, timezone
import urllib.request
import urllib.error
import urllib.parse
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from apps.api.models.market import MarketProduct, MarketListing, MarketPriceObservation
from apps.services.alerts.alert_engine import AlertEngine
from apps.services.gpu.models_hardware import GpuModel, CpuModel
from apps.api.core.config import settings

logger = logging.getLogger(__name__)

class RetailCrawler:
    """
    Real Web Crawler that scrapes actual retail market data using Naver Shopping API.
    """
    
    def __init__(self):
        self.api_url = "https://openapi.naver.com/v1/search/shop.json"
        self.client_id = settings.NAVER_SHOPPING_CLIENT_ID
        self.client_secret = settings.NAVER_SHOPPING_CLIENT_SECRET

    def get_seed_queries(self) -> List[str]:
        """
        Provides a diverse set of hardware keywords to kickstart the crawling process.
        The crawler will dynamically discover and register specific models found from these seeds.
        """
        return [
            # GPUs
            "RTX 4090", "RTX 4080 SUPER", "RTX 4070 Ti", "RX 7900 XTX",
            # CPUs
            "i9-14900K", "Ryzen 9 7950X3D", "i7-14700K", "Ryzen 7 7800X3D",
            # Server/AI GPUs
            "NVIDIA A100", "NVIDIA H100", "NVIDIA RTX 6000 Ada", "Tesla V100",
            # RAM
            "DDR5 32GB", "DDR5 64GB", "DDR4 32GB",
            # SSD
            "2TB NVMe M.2", "4TB NVMe SSD", "Samsung 990 PRO", "SK Hynix P41"
        ]

    async def search_naver_shopping(self, query: str) -> List[Dict[str, Any]]:
        """Search Naver Shopping for a given model."""
        if not self.client_id or not self.client_secret:
            logger.warning("Naver Shopping API keys not configured. Skipping real API call.")
            return []

        encText = urllib.parse.quote(query)
        url = f"{self.api_url}?query={encText}&display=5&sort=asc"
        
        req = urllib.request.Request(url)
        req.add_header("X-Naver-Client-Id", self.client_id)
        req.add_header("X-Naver-Client-Secret", self.client_secret)
        
        try:
            response = await asyncio.to_thread(urllib.request.urlopen, req)
            rescode = response.getcode()
            if rescode == 200:
                response_body = response.read()
                data = json.loads(response_body.decode('utf-8'))
                items = data.get("items", [])
                negative_keywords = ["쿨러", "파워", "케이스", "팬", "방열판", "수냉", "가이드", "브라켓", "케이블", "스티커", "박스", "공박스", "fan", "cooler", "heatsink", "water block"]
                filtered_items = []
                for item in items:
                    title = item.get("title", "").replace("<b>", "").replace("</b>", "").lower()
                    if any(kw in title for kw in negative_keywords):
                        continue
                    filtered_items.append(item)
                return filtered_items
            else:
                logger.error(f"Naver API error code: {rescode}")
                return []
        except Exception as e:
            logger.error(f"Failed to fetch from Naver API for query '{query}': {e}")
            return []

    async def sync_to_db(self, db: AsyncSession) -> Dict[str, Any]:
        models_to_search = self.get_seed_queries()
        
        if not self.client_id or not self.client_secret:
            return {
                "status": "error",
                "message": "NAVER_SHOPPING_CLIENT_ID or NAVER_SHOPPING_CLIENT_SECRET is missing. Cannot fetch real data."
            }
            
        inserted_products = 0
        inserted_prices = 0
        crawled_items = 0
        
        for query in models_to_search:
            logger.info(f"Crawling retail prices for seed: {query}")
            items = await self.search_naver_shopping(query)
            
            for item in items:
                crawled_items += 1
                
                # Naver API returns title with <b> tags
                title = item.get("title", "").replace("<b>", "").replace("</b>", "")
                link = item.get("link", "")
                mall_name = item.get("mallName", "Unknown")
                price_str = item.get("lprice", "0")
                
                try:
                    price = float(price_str)
                except ValueError:
                    continue
                    
                if price <= 0:
                    continue
                
                # Heuristic parsing for category and manufacturer from title & query
                search_text = f"{query} {title}".lower()
                
                category = "OTHER"
                if any(k in search_text for k in ["rtx", "rx 7", "rx 6", "gtx", "radeon"]):
                    category = "GPU"
                elif any(k in search_text for k in ["core i", "ryzen", "xeon", "epyc", "intel core"]):
                    category = "CPU"
                elif any(k in search_text for k in ["a100", "h100", "v100", "tesla", "rtx 6000", "l40"]):
                    category = "SERVER_GPU"
                elif any(k in search_text for k in ["ddr4", "ddr5", "ram", "메모리"]):
                    category = "RAM"
                elif any(k in search_text for k in ["ssd", "nvme", "m.2"]):
                    category = "SSD"
                    
                manufacturer = "Unknown"
                if any(k in search_text for k in ["nvidia", "지포스", "geforce"]): manufacturer = "NVIDIA"
                elif any(k in search_text for k in ["amd", "radeon", "ryzen", "epyc"]): manufacturer = "AMD"
                elif any(k in search_text for k in ["intel", "인텔", "xeon", "core"]): manufacturer = "Intel"
                elif any(k in search_text for k in ["samsung", "삼성"]): manufacturer = "Samsung"
                elif any(k in search_text for k in ["sk hynix", "하이닉스"]): manufacturer = "SK Hynix"
                elif any(k in search_text for k in ["micron", "마이크론", "crucial"]): manufacturer = "Micron"
                
                # 1. Upsert MarketProduct (Use the seed query as the standardized model_name for grouping)
                model_name = query
                
                stmt = select(MarketProduct).where(MarketProduct.model_name == model_name)
                result = await db.execute(stmt)
                product = result.scalar_one_or_none()
                
                if not product:
                    product = MarketProduct(
                        manufacturer=manufacturer,
                        model_name=model_name,
                        product_line=category,
                        category=category
                    )
                    db.add(product)
                    await db.flush()
                    inserted_products += 1
                    
                # 2. Upsert MarketListing
                stmt_listing = select(MarketListing).where(
                    (MarketListing.product_id == str(product.id)) & 
                    (MarketListing.vendor_name == mall_name) &
                    (MarketListing.url == link)
                )
                res_listing = await db.execute(stmt_listing)
                listing = res_listing.scalar_one_or_none()
                
                if not listing:
                    listing = MarketListing(
                        product_id=str(product.id),
                        vendor_name=mall_name,
                        original_title=title,
                        url=link,
                        condition="new"
                    )
                    db.add(listing)
                    await db.flush()
                    
                # 3. Insert Price Observation
                obs = MarketPriceObservation(
                    listing_id=str(listing.id),
                    price=price,
                    shipping_fee=0,
                    total_price=price,
                    currency="KRW",
                    in_stock=True,
                    observed_at=datetime.now(timezone.utc)
                )
                db.add(obs)
                inserted_prices += 1
                
                # Check for alerts
                alert_engine = AlertEngine()
                await alert_engine.check_retail_alerts(db, model_name, price, link)
                
        await db.commit()
        return {
            "status": "success", 
            "crawled_items": crawled_items,
            "inserted_products": inserted_products,
            "inserted_prices": inserted_prices
        }
