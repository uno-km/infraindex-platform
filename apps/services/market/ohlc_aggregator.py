"""
apps/services/market/ohlc_aggregator.py

Phase 1 — 리테일 가격 시계열을 일별 OHLC로 집계하는 서비스.

설계 원칙:
  - calculate_ohlc / ohlc_to_apexcharts / compute_summary 는 순수 함수 (DB 의존 없음)
  - OHLCAggregator 클래스는 DB 세션을 주입받아 집계 후 저장
"""
import logging
from datetime import date, datetime, timezone, timedelta
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import func, and_

from apps.api.models.market import MarketProduct, MarketListing, MarketPriceObservation
from apps.api.models.ohlc import MarketOHLCDaily

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# 순수 함수 계층 (Pure Functions — no DB, easy to test)
# ─────────────────────────────────────────────────────────────────────────────

def calculate_ohlc(prices: list[tuple[datetime, float]]) -> dict[str, Any]:
    """
    (timestamp, price) 튜플 리스트 → OHLC 딕셔너리 변환.

    Args:
        prices: [(datetime, price), ...] — 정렬 순서 무관

    Returns:
        {"open": float, "high": float, "low": float, "close": float,
         "avg": float, "volume": int}

    Raises:
        ValueError: prices 가 비어있을 때
    """
    if not prices:
        raise ValueError("prices must not be empty")

    # 시간 순서로 정렬
    sorted_prices = sorted(prices, key=lambda x: x[0])

    values = [p[1] for p in sorted_prices]

    return {
        "open": sorted_prices[0][1],
        "high": max(values),
        "low": min(values),
        "close": sorted_prices[-1][1],
        "avg": sum(values) / len(values),
        "volume": len(values),
    }


def ohlc_to_apexcharts(row: dict[str, Any]) -> dict[str, Any]:
    """
    OHLC DB row → ApexCharts candlestick 형식 변환.
    ApexCharts 형식: { x: "ISO date string", o, h, l, c }

    Args:
        row: {"trade_date": date, "open_price": float, "high_price": float,
              "low_price": float, "close_price": float}

    Returns:
        {"x": "2026-07-01", "o": float, "h": float, "l": float, "c": float}
    """
    trade_date = row["trade_date"]
    # date 또는 datetime 모두 처리
    if isinstance(trade_date, datetime):
        date_str = trade_date.date().isoformat()
    elif isinstance(trade_date, date):
        date_str = trade_date.isoformat()
    else:
        date_str = str(trade_date)

    return {
        "x": date_str,
        "o": row["open_price"],
        "h": row["high_price"],
        "l": row["low_price"],
        "c": row["close_price"],
    }


def compute_summary(ohlc_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """
    OHLC 시리즈로부터 요약 통계 계산.

    Args:
        ohlc_rows: [{"trade_date": date, "open_price": float,
                     "high_price": float, "low_price": float,
                     "close_price": float}, ...]

    Returns:
        {current_price, change_1d, change_pct_1d, all_time_high, all_time_low}
    """
    if not ohlc_rows:
        return {
            "current_price": 0,
            "change_1d": 0,
            "change_pct_1d": 0.0,
            "all_time_high": 0,
            "all_time_low": 0,
        }

    # 날짜 순 정렬 후 마지막 close = 현재가
    sorted_rows = sorted(ohlc_rows, key=lambda x: x["trade_date"])

    current = sorted_rows[-1]["close_price"]
    previous = sorted_rows[-2]["close_price"] if len(sorted_rows) >= 2 else current

    all_highs = [r["high_price"] for r in sorted_rows]
    all_lows = [r["low_price"] for r in sorted_rows]

    change_1d = current - previous
    change_pct_1d = (change_1d / previous * 100) if previous > 0 else 0.0

    return {
        "current_price": current,
        "change_1d": change_1d,
        "change_pct_1d": round(change_pct_1d, 2),
        "all_time_high": max(all_highs),
        "all_time_low": min(all_lows),
    }


# ─────────────────────────────────────────────────────────────────────────────
# DB 집계 클래스 (OHLCAggregator)
# ─────────────────────────────────────────────────────────────────────────────

class OHLCAggregator:
    """
    tbl_market_price_obs 데이터를 일 단위로 집계하여
    tbl_market_ohlc_daily 에 upsert 하는 집계기.

    Usage:
        aggregator = OHLCAggregator()
        async with get_db() as db:
            result = await aggregator.aggregate_daily(db, date.today() - timedelta(days=1))
    """

    async def _fetch_product_ids(self, db: AsyncSession) -> list[str]:
        """집계 대상 상품 ID 목록 조회"""
        stmt = select(MarketProduct.id)
        result = await db.execute(stmt)
        return [str(row[0]) for row in result.fetchall()]

    async def _fetch_observations(
        self, db: AsyncSession, product_id: str, target_date: date
    ) -> list[MarketPriceObservation]:
        """특정 상품·날짜의 가격 관측치 조회"""
        start = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=timezone.utc)
        end = start + timedelta(days=1)

        stmt = (
            select(MarketPriceObservation)
            .join(MarketListing, MarketListing.id == MarketPriceObservation.listing_id)
            .where(
                and_(
                    MarketListing.product_id == product_id,
                    MarketPriceObservation.observed_at >= start,
                    MarketPriceObservation.observed_at < end,
                )
            )
            .order_by(MarketPriceObservation.observed_at)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def _upsert_ohlc(
        self, db: AsyncSession, ohlc_data: dict[str, Any]
    ) -> None:
        """OHLC 데이터를 DB에 upsert (INSERT … ON CONFLICT DO UPDATE)"""
        stmt = pg_insert(MarketOHLCDaily).values(**ohlc_data)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_ohlc_product_date",
            set_={
                "open_price": stmt.excluded.open_price,
                "high_price": stmt.excluded.high_price,
                "low_price": stmt.excluded.low_price,
                "close_price": stmt.excluded.close_price,
                "avg_price": stmt.excluded.avg_price,
                "volume": stmt.excluded.volume,
            },
        )
        await db.execute(stmt)

    async def aggregate_daily(
        self, db: AsyncSession, target_date: date
    ) -> dict[str, Any]:
        """
        특정 날짜의 모든 상품에 대해 OHLC 집계 실행.

        Args:
            db: SQLAlchemy AsyncSession
            target_date: 집계할 날짜 (보통 어제)

        Returns:
            {"aggregated": int, "skipped": int}
        """
        product_ids = await self._fetch_product_ids(db)
        aggregated = 0
        skipped = 0

        for product_id in product_ids:
            observations = await self._fetch_observations(db, product_id, target_date)

            if not observations:
                skipped += 1
                continue

            prices = [(obs.observed_at, obs.price) for obs in observations]
            ohlc = calculate_ohlc(prices)

            # 판매처 수 (distinct listing_id 기준)
            listing_ids = {obs.listing_id for obs in observations}

            await self._upsert_ohlc(
                db,
                {
                    "product_id": product_id,
                    "trade_date": target_date,
                    "open_price": ohlc["open"],
                    "high_price": ohlc["high"],
                    "low_price": ohlc["low"],
                    "close_price": ohlc["close"],
                    "avg_price": ohlc["avg"],
                    "volume": ohlc["volume"],
                    "vendor_count": len(listing_ids),
                },
            )
            aggregated += 1

        await db.commit()
        logger.info(
            f"OHLC aggregation complete for {target_date}: "
            f"aggregated={aggregated}, skipped={skipped}"
        )
        return {"aggregated": aggregated, "skipped": skipped}

    async def backfill(
        self, db: AsyncSession, from_date: date, to_date: date
    ) -> dict[str, Any]:
        """
        날짜 범위 전체 OHLC 백필.
        최초 실행 또는 과거 데이터 복구 시 사용.

        Args:
            db: AsyncSession
            from_date: 시작일 (inclusive)
            to_date: 종료일 (inclusive)
        """
        total = 0
        current = from_date
        while current <= to_date:
            result = await self.aggregate_daily(db, current)
            total += result.get("aggregated", 0)
            current += timedelta(days=1)
        return {"total_aggregated": total, "from": str(from_date), "to": str(to_date)}
