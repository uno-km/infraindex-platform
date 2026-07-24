import os
import asyncio
from datetime import date, datetime
from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright

from shared.db.session import AsyncSessionLocal as async_session_factory
from sqlalchemy import select
from shared.models.reporter import DailyReport
from shared.models.market import MarketProduct, MarketPriceObservation
from shared.models.news import NewsArticle

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "storage", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

class PDFReporter:
    async def _fetch_market_data(self):
        """Fetch some dummy or recent market data for the report."""
        if not async_session_factory:
            return []
        async with async_session_factory() as session:
            # Query top 3 products
            stmt = select(MarketProduct).limit(3)
            result = await session.execute(stmt)
            products = result.scalars().all()
            
            market_data = []
            for p in products:
                # get latest price through listings
                from shared.models.market import MarketListing
                obs_stmt = (
                    select(MarketPriceObservation)
                    .join(MarketListing, MarketPriceObservation.listing_id == MarketListing.id)
                    .where(MarketListing.product_id == p.id)
                    .order_by(MarketPriceObservation.observed_at.desc())
                    .limit(1)
                )
                obs_result = await session.execute(obs_stmt)
                obs = obs_result.scalars().first()
                if obs:
                    market_data.append({
                        "model_name": p.model_name,
                        "price": obs.price,
                        "change": 0.0 # Placeholder
                    })
            return market_data

    async def _fetch_top_news(self):
        """Fetch top 5 recent news articles."""
        if not async_session_factory:
            return []
        async with async_session_factory() as session:
            stmt = select(NewsArticle).order_by(NewsArticle.published_at.desc()).limit(5)
            result = await session.execute(stmt)
            articles = result.scalars().all()
            
            top_news = []
            for a in articles:
                top_news.append({
                    "title": a.title,
                    "summary_ko": getattr(a, "summary_ko", a.summary),
                    "summary": a.summary
                })
            return top_news

    async def _build_context(self, report_date: date, report_type: str):
        market_data = await self._fetch_market_data()
        top_news = await self._fetch_top_news()
        
        return {
            "report_date": report_date.strftime("%Y-%m-%d"),
            "report_type": report_type,
            "market_data": market_data,
            "top_news": top_news,
            "ai_summary": "최근 수집된 데이터에 따르면 GPU 가격이 전반적으로 안정세를 보이고 있으며, 주요 반도체 기업들의 AI 인프라 투자 소식이 계속되고 있습니다.",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    async def generate_report(self, report_date: date, report_type: str) -> str:
        """Generates the PDF and saves it to local storage. Returns the file path."""
        context = await self._build_context(report_date, report_type)
        template_name = f"report_{report_type}.html"
        try:
            template = jinja_env.get_template(template_name)
        except Exception:
            # Fallback to morning if evening is missing
            template = jinja_env.get_template("report_morning.html")
            
        html_content = template.render(context)
        
        filename = f"AMEVA_Report_{report_date.strftime('%Y%m%d')}_{report_type}.pdf"
        file_path = os.path.join(REPORTS_DIR, filename)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.set_content(html_content, wait_until="networkidle")
            await page.pdf(path=file_path, format="A4", print_background=True, margin={"top": "20px", "bottom": "20px", "left": "20px", "right": "20px"})
            await browser.close()
            
        file_size = os.path.getsize(file_path)
        
        # Save to DB
        if async_session_factory:
            async with async_session_factory() as session:
                # Check if exists
                stmt = select(DailyReport).where(DailyReport.report_date == report_date, DailyReport.report_type == report_type)
                result = await session.execute(stmt)
                existing = result.scalars().first()
                
                if existing:
                    existing.file_path = f"/storage/reports/{filename}"
                    existing.file_size_bytes = file_size
                    existing.generated_at = datetime.utcnow()
                else:
                    new_report = DailyReport(
                        report_date=report_date,
                        report_type=report_type,
                        file_path=f"/storage/reports/{filename}",
                        file_size_bytes=file_size
                    )
                    session.add(new_report)
                await session.commit()
            
        return file_path
