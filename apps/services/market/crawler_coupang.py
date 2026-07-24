import os
import hmac
import hashlib
import urllib.request
import urllib.parse
import json
import logging
import time
from typing import List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apps.api.core.config import settings
from apps.api.models.market import MarketProduct, MarketListing, MarketPriceObservation
from apps.services.alerts.alert_engine import AlertEngine

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
                    items = data["data"].get("productData", [])
                    negative_keywords = [
                        # 쿨링 악세사리
                        "쿨러", "쿨링팬", "히트싱크", "방열판", "수냉", "수냉쿨러", "워터블록",
                        "팬", "blower", "cooler", "cooling fan", "heatsink", "water block", "fan",
                        # 케이스/브라켓
                        "케이스", "브라켓", "홀더", "거치대", "받침대",
                        # 케이블/악세사리
                        "케이블", "어댑터", "젠더", "커넥터", "파워케이블",
                        # 비GPU 부품
                        "마우스", "키보드", "모니터", "헤드셋",
                    ]
                    filtered_items = []
                    for item in items:
                        name = item.get("productName", "").lower()
                        if any(kw in name for kw in negative_keywords):
                            continue
                        filtered_items.append(item)
                    return filtered_items
                else:
                    logger.warning(f"Coupang API Error: {data.get('rMessage')}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching from Coupang API: {e}")
            return []

    def get_seed_queries(self) -> List[str]:
        return [
            # GPUs
            "RTX 4090", "RTX 4080 SUPER", "RTX 4070 Ti", "RX 7900 XTX",
            # CPUs
            "i9-14900K", "Ryzen 9 7950X3D", "i7-14700K", "Ryzen 7 7800X3D",
            # RAM
            "DDR5 32GB", "DDR5 64GB", "DDR4 32GB",
            # SSD
            "2TB NVMe M.2", "4TB NVMe SSD", "Samsung 990 PRO", "SK Hynix P41"
        ]

    async def sync_to_db(self, db: AsyncSession):
        if not self.access_key or not self.secret_key:
            return {"status": "error", "message": "COUPANG_ACCESS_KEY or COUPANG_SECRET_KEY is missing."}

        models_to_search = self.get_seed_queries()
        
        total_inserted = 0
        now = datetime.now(timezone.utc)

        for query in models_to_search:
            logger.info(f"Crawling Coupang prices for seed: {query}")
            items = self.search_products(query, limit=5)
            
            for item in items:
                vendor = "Coupang 로켓배송" if item.get("isRocket") else "Coupang"
                price = int(item.get("productPrice", 0))
                title = item.get("productName", "")
                link = item.get("productUrl", "")
                
                if price <= 0:
                    continue
                
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
                
                # Create Listing
                stmt_listing = select(MarketListing).where(
                    (MarketListing.product_id == str(product.id)) & 
                    (MarketListing.vendor_name == vendor) &
                    (MarketListing.url == link)
                )
                res_listing = await db.execute(stmt_listing)
                listing = res_listing.scalar_one_or_none()
                
                if not listing:
                    listing = MarketListing(
                        product_id=str(product.id),
                        vendor_name=vendor,
                        original_title=title,
                        url=link,
                        condition="new"
                    )
                    db.add(listing)
                    await db.flush()
                
                # Create Price Observation
                obs = MarketPriceObservation(
                    listing_id=str(listing.id),
                    price=price,
                    shipping_fee=0 if item.get("isFreeShipping") else 3000,
                    total_price=price + (0 if item.get("isFreeShipping") else 3000),
                    currency="KRW",
                    in_stock=True,
                    observed_at=now
                )
                db.add(obs)
                total_inserted += 1
                
                # Check for alerts
                alert_engine = AlertEngine()
                await alert_engine.check_retail_alerts(db, model_name, price, link)

        await db.commit()
        return {"status": "success", "crawled_items": total_inserted}
