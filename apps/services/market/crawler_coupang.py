import os
import hmac
import hashlib
import urllib.request
import urllib.parse
import json
import logging
import time
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apps.api.core.config import settings
from apps.api.models.market import MarketProduct, MarketListing, MarketPriceObservation

logger = logging.getLogger(__name__)

class CoupangCrawler:
    def __init__(self):
        self.access_key = settings.COUPANG_ACCESS_KEY
        self.secret_key = settings.COUPANG_SECRET_KEY
        self.api_url = "https://api-gateway.coupang.com"

    def _generate_hmac(self, method: str, url_path: str, query: str = "") -> str:
        datetime_str = time.strftime('%y%m%d', time.gmtime()) + "T" + time.strftime('%H%M%S', time.gmtime()) + "Z"
        message = datetime_str + method + url_path + query
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return f"CEA algorithm=HmacSHA256, access-key={self.access_key}, signed-date={datetime_str}, signature={signature}"

    def search_products(self, keyword: str, limit: int = 5):
        if not self.access_key or not self.secret_key:
            logger.error("Coupang API keys are missing.")
            return []

        method = "GET"
        url_path = "/v2/providers/affiliate_open_api/apis/openapi/products/search"
        query_dict = {"keyword": keyword, "limit": limit}
        query_str = urllib.parse.urlencode(query_dict)
        
        url = f"{self.api_url}{url_path}?{query_str}"
        authorization = self._generate_hmac(method, url_path, query_str)
        
        req = urllib.request.Request(url)
        req.add_header("Authorization", authorization)
        req.add_header("Content-Type", "application/json;charset=UTF-8")

        try:
            with urllib.request.urlopen(req) as response:
                res_data = response.read().decode('utf-8')
                data = json.loads(res_data)
                if data.get("rCode") == "0" and "data" in data:
                    return data["data"].get("productData", [])
                else:
                    logger.warning(f"Coupang API Error: {data.get('rMessage')}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching from Coupang API: {e}")
            return []

    async def sync_to_db(self, db: AsyncSession):
        if not self.access_key or not self.secret_key:
            return {"status": "error", "message": "COUPANG_ACCESS_KEY or COUPANG_SECRET_KEY is missing."}

        stmt = select(MarketProduct)
        result = await db.execute(stmt)
        products = result.scalars().all()

        fallback_models = []
        if not products:
            logger.warning("No models found in MarketProduct. Using fallback list.")
            fallback_models = [
                {"id": "mock_4090", "model_name": "RTX 4090", "manufacturer": "NVIDIA", "category": "GPU"},
                {"id": "mock_4080", "model_name": "RTX 4080", "manufacturer": "NVIDIA", "category": "GPU"},
                {"id": "mock_14900k", "model_name": "i9-14900K", "manufacturer": "Intel", "category": "CPU"},
            ]
        
        items_to_search = products if products else fallback_models
        
        total_inserted = 0
        now = datetime.now(timezone.utc)

        for p in items_to_search:
            product_id = str(p.id) if hasattr(p, 'id') else p["id"]
            model_name = p.model_name if hasattr(p, 'model_name') else p["model_name"]
            
            logger.info(f"Crawling Coupang prices for: {model_name}")
            items = self.search_products(model_name, limit=5)
            
            for item in items:
                vendor = "Coupang 로켓배송" if item.get("isRocket") else "Coupang"
                price = int(item.get("productPrice", 0))
                if price <= 0:
                    continue
                
                # Create Listing
                listing = MarketListing(
                    product_id=product_id,
                    vendor_name=vendor,
                    original_title=item.get("productName", model_name),
                    url=item.get("productUrl", ""),
                    condition="new"
                )
                db.add(listing)
                await db.flush() # get listing id
                
                # Create Price Observation
                obs = MarketPriceObservation(
                    listing_id=listing.id,
                    price=price,
                    shipping_fee=0 if item.get("isFreeShipping") else 3000,
                    total_price=price + (0 if item.get("isFreeShipping") else 3000),
                    currency="KRW",
                    in_stock=True,
                    observed_at=now
                )
                db.add(obs)
                total_inserted += 1

        await db.commit()
        return {"status": "success", "crawled_items": total_inserted}
