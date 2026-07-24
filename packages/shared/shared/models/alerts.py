from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from shared.models.base import Base

class AlertRule(Base):
    """
    User-defined alert rules.
    """
    __tablename__ = "tbl_alert_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Target can be a product ID or a keyword, depending on the rule type
    target = Column(String(255), nullable=False)
    # Type of alert: 'retail_price', 'news_keyword'
    alert_type = Column(String(50), nullable=False)
    
    # Specific condition (e.g. "< 2000000" for price)
    # Using a simple threshold float for retail price alerts
    price_threshold = Column(Float, nullable=True)
    
    # Whether this rule is active
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class AlertHistory(Base):
    """
    Record of alerts that were triggered.
    """
    __tablename__ = "tbl_alert_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_id = Column(UUID(as_uuid=True), ForeignKey("tbl_alert_rules.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String(255), nullable=False)
    message = Column(String, nullable=False)
    
    # Context link, e.g. URL to the product or news article
    link_url = Column(String, nullable=True)
    
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
