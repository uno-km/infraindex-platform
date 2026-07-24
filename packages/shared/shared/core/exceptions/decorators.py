import functools
import traceback
import logging
from typing import Callable, Any, Coroutine
from shared.db.session import AsyncSessionLocal
from shared.models.error_log import ErrorLog
from shared.services.telegram_notifier import send_telegram_message

logger = logging.getLogger(__name__)

def notify_on_error(severity: str = "NORMAL", source: str = "unknown"):
    """
    예외 발생 시 ErrorLog DB에 적재하고, CRITICAL일 경우 즉시 텔레그램 발송.
    """
    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                error_msg = str(e)
                trace = traceback.format_exc()
                error_type = e.__class__.__name__

                # DB 기록 (세션 분리)
                if AsyncSessionLocal:
                    try:
                        async with AsyncSessionLocal() as session:
                            error_log = ErrorLog(
                                severity=severity,
                                source=source,
                                error_type=error_type,
                                error_message=error_msg,
                                traceback=trace,
                                is_sent=False
                            )
                            session.add(error_log)
                            await session.commit()
                    except Exception as db_e:
                        logger.error(f"Failed to save ErrorLog to DB: {db_e}")
                else:
                    logger.warning("AsyncSessionLocal not initialized, skipping DB error log.")

                # 즉시 발송
                if severity == "CRITICAL":
                    alert_msg = (
                        f"🚨 <b>[CRITICAL ERROR]</b>\n"
                        f"<b>Source:</b> {source}\n"
                        f"<b>Type:</b> {error_type}\n"
                        f"<b>Message:</b> <code>{error_msg}</code>"
                    )
                    # For critical, send instantly but don't block
                    # Ensure telegram is sent
                    await send_telegram_message(alert_msg)
                
                # Re-raise the exception after logging
                raise
        return wrapper
    return decorator
