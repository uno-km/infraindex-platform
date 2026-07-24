import pytest
from unittest.mock import AsyncMock, patch
from apps.batch.services.ai_pricing.crawler_html import crawl_html_pricing
from shared.models.error_log import ErrorLog

@pytest.mark.asyncio
async def test_crawl_html_pricing_failure_sends_telegram():
    """
    CSS 셀렉터가 변경되어 가격을 파싱하지 못했을 때,
    @notify_on_error(severity="CRITICAL") 데코레이터가 작동하여
    ErrorLog 기록 및 Telegram 발송을 수행하는지 테스트합니다.
    """
    mock_html = "<html><body><div class='wrong-class'>Price $3.00</div></body></html>"

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.text = mock_html
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        with patch('shared.core.exceptions.decorators.send_telegram_message', new_callable=AsyncMock) as mock_send:
            with patch('shared.core.exceptions.decorators.AsyncSessionLocal') as mock_session_maker:
                
                # Setup DB Mock
                mock_session = AsyncMock()
                mock_session_maker.return_value.__aenter__.return_value = mock_session

                # 실행 시 예외가 발생(raise_for_status 또는 ValueError)해야 정상
                with pytest.raises(ValueError, match="Anthropic Pricing table CSS selector.*not found"):
                    await crawl_html_pricing()

                # DB 저장 호출 검증
                mock_session.add.assert_called_once()
                added_arg = mock_session.add.call_args[0][0]
                assert isinstance(added_arg, ErrorLog)
                assert added_arg.severity == "CRITICAL"
                assert added_arg.source == "crawler_html_fallback"
                assert added_arg.error_type == "ValueError"

                # 텔레그램 발송 호출 검증 (CRITICAL이므로 즉시 발송)
                mock_send.assert_called_once()
                sent_msg = mock_send.call_args[0][0]
                assert "[CRITICAL ERROR]" in sent_msg
                assert "ValueError" in sent_msg
                assert "Anthropic Pricing table CSS selector" in sent_msg
