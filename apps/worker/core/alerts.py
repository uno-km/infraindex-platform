import httpx
import logging
import os

logger = logging.getLogger(__name__)

# Fallback webhook URL for scaffold testing
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")

async def send_critical_alert(title: str, message: str, provider: str = "Unknown"):
    """
    Sends a webhook alert to Discord or Telegram when a crawler fails critically
    (e.g., CAPTCHA blocked, API structure changed).
    """
    logger.error(f"[ALERT] {provider} - {title}: {message}")
    
    if not DISCORD_WEBHOOK_URL:
        return
        
    payload = {
        "content": f"🚨 **CRITICAL ALERT: {provider}** 🚨\n**{title}**\n```{message}```"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            await client.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5.0)
    except Exception as e:
        logger.error(f"Failed to send Discord alert: {str(e)}")
