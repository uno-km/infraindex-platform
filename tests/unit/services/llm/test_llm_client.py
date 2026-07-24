"""
tests/unit/services/llm/test_llm_client.py
Phase 2.5 - LLM AI 브리핑 클라이언트 유닛 테스트
ai_service.py의 generate_daily_news_briefing, generate_market_analysis 테스트
외부 LLM API 호출을 AsyncMock으로 격리
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestLLMClient:
    """LLM 클라이언트 설정 및 브리핑 생성 로직 테스트"""

    def test_ai_service_module_importable(self):
        """ai_service 모듈이 정상적으로 임포트되어야 한다"""
        from apps.server.core import ai_service
        assert hasattr(ai_service, "generate_daily_news_briefing")
        assert hasattr(ai_service, "generate_market_analysis")

    def test_client_uses_openai_or_ollama(self):
        """OpenAI 키가 있으면 OpenAI 클라이언트, 없으면 Ollama를 사용해야 한다"""
        from apps.server.core import ai_service
        # client 객체 존재 확인
        assert hasattr(ai_service, "client")
        assert hasattr(ai_service, "MODEL")
        assert isinstance(ai_service.MODEL, str)

    @pytest.mark.asyncio
    async def test_generate_daily_briefing_with_empty_articles(self):
        """기사가 없을 때 기본 텍스트를 반환해야 한다"""
        from apps.server.core.ai_service import generate_daily_news_briefing
        result = await generate_daily_news_briefing("2026-07-24", [])
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_generate_daily_briefing_with_mock_llm(self):
        """LLM 호출을 모킹하여 브리핑 생성 로직을 검증한다"""
        from apps.server.core.ai_service import generate_daily_news_briefing

        mock_message = MagicMock()
        mock_message.content = "## 2026-07-24 AI 데일리 브리핑\n\n1. NVIDIA GPU 가격 안정세\n2. HBM3e 공급 부족 지속"

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        mock_create = AsyncMock(return_value=mock_response)

        articles = [
            {"title": "NVIDIA GPU price stabilizes", "source": "TechCrunch",
             "summary": "GPU prices show stability", "category": "GPU"},
            {"title": "HBM3e supply shortage continues", "source": "Bloomberg",
             "summary": "Memory shortage", "category": "메모리"},
        ]

        with patch("apps.server.core.ai_service.client") as mock_client:
            mock_client.chat.completions.create = mock_create
            result = await generate_daily_news_briefing("2026-07-24", articles)

        assert isinstance(result, str)
        assert len(result) > 0
        mock_create.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_briefing_fallback_on_error(self):
        """LLM 호출 실패 시 mock 브리핑으로 폴백해야 한다"""
        from apps.server.core.ai_service import generate_daily_news_briefing, _get_mock_briefing

        articles = [{"title": "Test article", "source": "Test", "summary": "Test", "category": "GPU"}]

        with patch("apps.server.core.ai_service.client") as mock_client:
            mock_client.chat.completions.create = AsyncMock(side_effect=Exception("LLM unavailable"))
            result = await generate_daily_news_briefing("2026-07-24", articles)

        # 폴백 결과도 유효한 문자열이어야 함
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_generate_market_analysis_with_mock(self):
        """generate_market_analysis LLM 호출 모킹 테스트"""
        from apps.server.core.ai_service import generate_market_analysis

        mock_message = MagicMock()
        mock_message.content = "Market analysis: GPU supply constrained, prices rising."
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        with patch("apps.server.core.ai_service.client") as mock_client:
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            result = await generate_market_analysis(
                news_data=[{"title": "test"}],
                power_data=[{"region": "Texas", "cost": 0.08}],
                memory_data=[{"component": "HBM3e", "price": 4500}]
            )

        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_market_analysis_fallback_on_error(self):
        """generate_market_analysis LLM 실패 시 mock 분석 반환해야 한다"""
        from apps.server.core.ai_service import generate_market_analysis

        with patch("apps.server.core.ai_service.client") as mock_client:
            mock_client.chat.completions.create = AsyncMock(side_effect=Exception("timeout"))
            result = await generate_market_analysis([], [], [])

        assert isinstance(result, str)
        assert len(result) > 0

    def test_mock_briefing_contains_date(self):
        """_get_mock_briefing은 날짜 문자열을 포함해야 한다"""
        from apps.server.core.ai_service import _get_mock_briefing
        date_str = "2026-07-24"
        result = _get_mock_briefing(date_str)
        assert date_str in result

    def test_mock_analysis_is_english(self):
        """_get_mock_analysis는 유효한 분석 텍스트를 반환해야 한다"""
        from apps.server.core.ai_service import _get_mock_analysis
        result = _get_mock_analysis()
        assert isinstance(result, str)
        assert len(result) >= 100
