"""
scripts/backfill_ohlc.py

Phase 1 — 기존 tbl_market_price_obs 데이터로 OHLC 집계 백필 스크립트.
최초 1회 실행하여 과거 데이터를 tbl_market_ohlc_daily 에 채웁니다.

사용법:
    python scripts/backfill_ohlc.py
    python scripts/backfill_ohlc.py --from 2026-01-01 --to 2026-07-23
"""
import asyncio
import argparse
import logging
import sys
import os
from datetime import date

# 프로젝트 루트를 파이썬 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


async def run(from_date: date, to_date: date):
    from apps.api.core.database import _build_engine, _build_session_factory
    from apps.services.market.ohlc_aggregator import OHLCAggregator

    engine = _build_engine()
    SessionLocal = _build_session_factory(engine)

    aggregator = OHLCAggregator()

    async with SessionLocal() as db:
        logger.info(f"Starting OHLC backfill from {from_date} to {to_date}...")
        result = await aggregator.backfill(db, from_date, to_date)
        logger.info(f"Backfill complete: {result}")


def main():
    parser = argparse.ArgumentParser(description="OHLC Backfill Script")
    parser.add_argument(
        "--from", dest="from_date",
        default=str(date.today().replace(month=1, day=1)),
        help="시작일 YYYY-MM-DD (기본: 올해 1월 1일)"
    )
    parser.add_argument(
        "--to", dest="to_date",
        default=str(date.today()),
        help="종료일 YYYY-MM-DD (기본: 오늘)"
    )

    args = parser.parse_args()
    from_date = date.fromisoformat(args.from_date)
    to_date = date.fromisoformat(args.to_date)

    asyncio.run(run(from_date, to_date))


if __name__ == "__main__":
    main()
