"""
tests/unit/api/test_alerts_api.py
Phase 4 - 알림 API 유닛 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
import uuid


class TestAlertsAPI:
    """알림 API 엔드포인트 유닛 테스트"""

    def test_alerts_router_importable(self):
        """alerts router가 임포트 가능해야 한다"""
        from apps.server.api.v1.endpoints.alerts import router
        assert router is not None

    def test_rules_route_exists(self):
        """/rules 라우트가 등록되어야 한다"""
        from apps.server.api.v1.endpoints.alerts import router
        routes = [r.path for r in router.routes]
        assert any("rules" in r for r in routes), f"rules 라우트 없음: {routes}"

    def test_history_route_exists(self):
        """/history 라우트가 등록되어야 한다"""
        from apps.server.api.v1.endpoints.alerts import router
        routes = [r.path for r in router.routes]
        assert any("history" in r for r in routes), f"history 라우트 없음: {routes}"

    def test_history_read_route_exists(self):
        """/history/{id}/read POST 라우트가 등록되어야 한다"""
        from apps.server.api.v1.endpoints.alerts import router
        routes = [r.path for r in router.routes]
        assert any("read" in r for r in routes), f"history/read 라우트 없음: {routes}"

    @pytest.mark.asyncio
    async def test_get_alert_rules_returns_list(self):
        """GET /rules는 리스트를 반환해야 한다"""
        from apps.server.api.v1.endpoints.alerts import get_alert_rules

        mock_rule = MagicMock()
        mock_rule.id = uuid.uuid4()
        mock_rule.target = "RTX 4090"
        mock_rule.alert_type = "retail_price"
        mock_rule.price_threshold = 2_000_000.0
        mock_rule.is_active = True

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_rule]
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await get_alert_rules(db=mock_db)
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_create_alert_rule(self):
        """POST /rules로 알림 규칙을 생성할 수 있어야 한다"""
        from apps.server.api.v1.endpoints.alerts import create_alert_rule, AlertRuleCreate

        rule_data = AlertRuleCreate(
            target="RTX 4090",
            alert_type="retail_price",
            price_threshold=2_000_000.0,
            is_active=True
        )

        mock_new_rule = MagicMock()
        mock_new_rule.id = uuid.uuid4()
        mock_new_rule.target = "RTX 4090"
        mock_new_rule.alert_type = "retail_price"
        mock_new_rule.price_threshold = 2_000_000.0
        mock_new_rule.is_active = True

        mock_db = AsyncMock()
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock(side_effect=lambda r: setattr(r, "id", uuid.uuid4()))

        with MagicMock() as mock_alert_rule:
            from unittest.mock import patch
            with patch("apps.server.api.v1.endpoints.alerts.AlertRule") as MockRule:
                MockRule.return_value = mock_new_rule
                result = await create_alert_rule(rule_in=rule_data, db=mock_db)

        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_alert_history_returns_list(self):
        """GET /history는 리스트를 반환해야 한다"""
        from apps.server.api.v1.endpoints.alerts import get_alert_history

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(return_value=mock_result)

        result = await get_alert_history(db=mock_db)
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_mark_alert_read_not_found(self):
        """존재하지 않는 alert history에 read 요청 시 404가 발생해야 한다"""
        from apps.server.api.v1.endpoints.alerts import mark_alert_read
        from fastapi import HTTPException

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_result)

        with pytest.raises(HTTPException) as exc_info:
            await mark_alert_read(history_id=uuid.uuid4(), db=mock_db)

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_mark_alert_read_success(self):
        """존재하는 alert history에 read 요청 시 is_read=True로 업데이트되어야 한다"""
        from apps.server.api.v1.endpoints.alerts import mark_alert_read

        mock_history = MagicMock()
        mock_history.id = uuid.uuid4()
        mock_history.rule_id = uuid.uuid4()
        mock_history.title = "Price Drop Alert"
        mock_history.message = "RTX 4090 is now 1,900,000 KRW"
        mock_history.link_url = None
        mock_history.is_read = False

        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_history
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        await mark_alert_read(history_id=mock_history.id, db=mock_db)

        assert mock_history.is_read is True
        mock_db.commit.assert_called_once()
