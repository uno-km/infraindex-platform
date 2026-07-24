import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from shared.models.alerts import AlertRule, AlertHistory

logger = logging.getLogger(__name__)

class AlertEngine:
    async def check_retail_alerts(self, db: AsyncSession, product_name: str, new_price: float, link_url: str):
        """
        Check if the new price triggers any retail price alert rules.
        """
        stmt = select(AlertRule).where(
            AlertRule.alert_type == "retail_price",
            AlertRule.target == product_name,
            AlertRule.is_active == True
        )
        result = await db.execute(stmt)
        rules = result.scalars().all()
        
        triggered_alerts = []
        for rule in rules:
            if rule.price_threshold is not None and new_price <= rule.price_threshold:
                # Triggered
                history = AlertHistory(
                    rule_id=rule.id,
                    title=f"Price Drop Alert: {product_name}",
                    message=f"{product_name} is now available at {new_price:,.0f} KRW (Target: {rule.price_threshold:,.0f} KRW).",
                    link_url=link_url
                )
                db.add(history)
                triggered_alerts.append(history)
                logger.info(f"Triggered Alert for {product_name}: {new_price} <= {rule.price_threshold}")
        
        if triggered_alerts:
            await db.commit()
            
        return triggered_alerts

    async def check_news_alerts(self, db: AsyncSession, article):
        """
        Check if the news article triggers any keyword alert rules.
        """
        stmt = select(AlertRule).where(
            AlertRule.alert_type == "news_keyword",
            AlertRule.is_active == True
        )
        result = await db.execute(stmt)
        rules = result.scalars().all()
        
        title_lower = (article.title or "").lower()
        
        triggered_alerts = []
        for rule in rules:
            target_lower = rule.target.lower()
            if target_lower in title_lower:
                history = AlertHistory(
                    rule_id=rule.id,
                    title=f"News Alert: {rule.target}",
                    message=f"A new article mentions '{rule.target}': {article.title}",
                    link_url=getattr(article, "url", None)
                )
                db.add(history)
                triggered_alerts.append(history)
                logger.info(f"Triggered News Alert for '{rule.target}' on article '{article.title}'")
        
        if triggered_alerts:
            await db.commit()
            
        return triggered_alerts
