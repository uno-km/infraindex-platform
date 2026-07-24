import asyncio
import logging
from sqlalchemy.future import select
from shared.db.session import AsyncSessionLocal
from shared.models.error_log import ErrorLog
from apps.server.core.ai_service import summarize_error_logs
from shared.services.telegram_notifier import send_telegram_message

logger = logging.getLogger(__name__)

async def generate_daily_error_report():
    """
    미발송 상태(is_sent=False)인 ErrorLog를 조회하여,
    LLM 요약을 거친 후 텔레그램으로 발송하고, 상태를 업데이트합니다.
    """
    logger.info("Starting Daily Error Report Generation...")
    
    if not AsyncSessionLocal:
        logger.warning("AsyncSessionLocal not initialized, cannot generate error report.")
        return

    async with AsyncSessionLocal() as session:
        # Fetch un-sent logs
        stmt = select(ErrorLog).where(ErrorLog.is_sent == False)
        result = await session.execute(stmt)
        un_sent_logs = result.scalars().all()

        if not un_sent_logs:
            logger.info("No un-sent error logs found. Skipping daily report.")
            return

        # Generate summary using LLM
        summary_markdown = await summarize_error_logs(un_sent_logs)
        
        # Add Header
        final_message = f"📊 <b>[Daily System Error Report]</b>\n\n{summary_markdown}"

        # Send Telegram Message
        success = await send_telegram_message(final_message)

        # Mark as sent if successful
        if success:
            for log in un_sent_logs:
                log.is_sent = True
            await session.commit()
            logger.info(f"Successfully processed and marked {len(un_sent_logs)} error logs as sent.")
        else:
            logger.error("Failed to send daily error report via Telegram.")

def run_daily_error_report():
    """Celery에서 동기적으로 호출하기 위한 래퍼 함수"""
    asyncio.run(generate_daily_error_report())
