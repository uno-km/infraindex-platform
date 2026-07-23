import asyncio
import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from apps.services.paper.crawler_arxiv import ArXivCrawler

async def main():
    crawler = ArXivCrawler()
    papers = await crawler.fetch_recent(max_results=3)
    for p in papers:
        print(p["external_id"], p["title"])

if __name__ == "__main__":
    asyncio.run(main())
