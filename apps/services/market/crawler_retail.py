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

    async def fetch_models(self, db: AsyncSession) -> List[str]:
        """Fetch all GPU and CPU model names from the database."""
        models = []
        
        # Get GPU models
        gpu_stmt = select(GpuModel.name)
        gpu_res = await db.execute(gpu_stmt)
        for row in gpu_res.scalars():
            models.append(row)
            
        # Get CPU models
        cpu_stmt = select(CpuModel.name)
        cpu_res = await db.execute(cpu_stmt)
        for row in cpu_res.scalars():
            models.append(row)
            
        # Fallback if DB is empty for hardware models
        if not models:
            logger.warning("No models found in GpuModel or CpuModel tables. Using fallback list.")
            models = ["RTX 4090", "RTX 4080", "i9-14900K", "Ryzen 9 7950X"]
            
        return models

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
        models_to_search = await self.fetch_models(db)
        
        if not self.client_id or not self.client_secret:
            return {
                "status": "error",
                "message": "NAVER_SHOPPING_CLIENT_ID or NAVER_SHOPPING_CLIENT_SECRET is missing. Cannot fetch real data."
            }
            
        inserted_products = 0
        inserted_prices = 0
        crawled_items = 0
        
        for model_name in models_to_search:
            logger.info(f"Crawling retail prices for: {model_name}")
            items = await self.search_naver_shopping(model_name)
            
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
                
                # Determine category heuristically
                category = "CPU" if "intel" in model_name.lower() or "ryzen" in model_name.lower() else "GPU"
                
                # 1. Upsert MarketProduct
                stmt = select(MarketProduct).where(MarketProduct.model_name == model_name)
                result = await db.execute(stmt)
                product = result.scalar_one_or_none()
                
                if not product:
                    product = MarketProduct(
                        manufacturer="Unknown", # Will need better parsing in the future
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
