"""
scripts/backfill_news.py
Phase 8 - 히스토리컬 뉴스 백필 CLI 스크립트

사용법:
    python scripts/backfill_news.py --from 2022-01-01 --to 2024-12-31
    python scripts/backfill_news.py --from 2023-01-01 --to 2023-12-31 --source arxiv --dry-run
    python scripts/backfill_news.py --from 2022-01-01 --to 2022-12-31 --source all --max-results 50
"""
import argparse
import asyncio
import logging
import sys
from datetime import date

# 프로젝트 루트를 sys.path에 추가
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("backfill")


def parse_args():
    parser = argparse.ArgumentParser(
        description="AMEVA 히스토리컬 뉴스/논문 백필 스크립트"
    )
    parser.add_argument(
        "--from", dest="from_date", required=True,
        help="시작 날짜 (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--to", dest="to_date", required=True,
        help="종료 날짜 (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--source", default="arxiv",
        choices=["arxiv", "sitemap", "all"],
        help="수집 소스 (기본: arxiv)"
    )
    parser.add_argument(
        "--max-results", type=int, default=100,
        help="월별 최대 수집 건수 (기본: 100)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="실제 저장 없이 수집 결과만 출력"
    )
    parser.add_argument(
        "--rate-limit", type=float, default=2.0,
        help="API 호출 간격 (초, 기본: 2.0)"
    )
    parser.add_argument(
        "--sitemap-url", default=None,
        help="--source=sitemap 사용 시 sitemap.xml URL"
    )
    return parser.parse_args()


async def run_backfill(args):
    from apps.batch.services.news.crawler_historical import HistoricalCrawler, date_range_months
    from apps.batch.services.news.duplicate_detector import DuplicateDetector

    from_date = date.fromisoformat(args.from_date)
    to_date = date.fromisoformat(args.to_date)

    if from_date > to_date:
        logger.error("--from 날짜가 --to 날짜보다 늦습니다.")
        sys.exit(1)

    logger.info(f"=== Phase 8 백필 시작 ===")
    logger.info(f"소스: {args.source}")
    logger.info(f"기간: {from_date} ~ {to_date}")
    logger.info(f"월별 최대: {args.max_results}건")
    logger.info(f"Dry-run: {args.dry_run}")

    crawler = HistoricalCrawler(rate_limit_seconds=args.rate_limit)
    detector = DuplicateDetector(similarity_threshold=0.85)

    total_fetched = 0
    total_new = 0
    total_duplicate = 0

    try:
        if args.source in ("arxiv", "all"):
            logger.info("[arXiv] 히스토리컬 논문 수집 시작...")
            papers = await crawler.fetch_arxiv_historical(
                from_date=from_date,
                to_date=to_date,
                max_results=args.max_results,
            )
            total_fetched += len(papers)
            logger.info(f"[arXiv] {len(papers)}건 수집됨")

            for paper in papers:
                article = {"url": paper.get("url", ""), "title": paper.get("title", "")}
                if detector.is_duplicate(article):
                    total_duplicate += 1
                else:
                    detector.register_article(article)
                    total_new += 1
                    if args.dry_run:
                        logger.info(f"  [DRY-RUN] 신규: {paper.get('title', '')[:80]}")

        if args.source in ("sitemap", "all") and args.sitemap_url:
            logger.info(f"[Sitemap] URL 수집 시작: {args.sitemap_url}")
            urls = await crawler.fetch_sitemap_urls(
                sitemap_url=args.sitemap_url,
                from_date=from_date,
                to_date=to_date,
            )
            total_fetched += len(urls)
            logger.info(f"[Sitemap] {len(urls)}개 URL 수집됨")

            for url in urls:
                article = {"url": url, "title": ""}
                if detector.is_duplicate(article):
                    total_duplicate += 1
                else:
                    detector.register_article(article)
                    total_new += 1

    except KeyboardInterrupt:
        logger.warning("사용자에 의해 중단됨")
    finally:
        await crawler.close()

    # 결과 요약
    logger.info("=== 백필 완료 ===")
    logger.info(f"총 수집: {total_fetched}건")
    logger.info(f"신규:    {total_new}건")
    logger.info(f"중복:    {total_duplicate}건")
    logger.info(f"캐시:    {detector.cache_size}")

    if args.dry_run:
        logger.info("[DRY-RUN] 실제 DB 저장은 수행되지 않았습니다.")

    return {"fetched": total_fetched, "new": total_new, "duplicate": total_duplicate}


def main():
    args = parse_args()
    result = asyncio.run(run_backfill(args))
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
