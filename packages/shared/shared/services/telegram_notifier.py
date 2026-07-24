import httpx
import logging
from shared.config.settings import settings

logger = logging.getLogger(__name__)

async def send_telegram_message(message: str) -> bool:
    """
    텔레그램 봇 API를 통해 메시지를 전송합니다.
    """
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not token or not chat_id:
        logger.warning("Telegram Bot Token or Chat ID is not configured. Skipping alert.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            response.raise_for_status()
            logger.info("Successfully sent Telegram alert.")
            return True
    except Exception as e:
        logger.error(f"Failed to send Telegram alert: {e}")
        return False
