import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import os

async def run_e2e_crawler():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"qa_e2e_{timestamp}.md")
    
    print("Starting Playwright E2E UI Crawler...")
    
    console_errors = []
    failed_requests = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Listen for console errors
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        
        # Listen for failed network responses (500s)
        page.on("response", lambda response: failed_requests.append(f"{response.status} - {response.url}") if response.status >= 500 else None)
        
        try:
            print("Navigating to http://localhost:3000 ...")
            await page.goto("http://localhost:3000", wait_until="networkidle", timeout=15000)
            
            # Interact with UI elements - wait for tabs and click them
            tabs = ["Retail Market", "Enterprise AI", "Global News", "Market Insights"]
            for tab in tabs:
                print(f"Clicking on tab: {tab}")
                try:
                    await page.click(f"text={tab}", timeout=5000)
                    await page.wait_for_timeout(2000) # Wait for re-render
                except Exception as e:
                    console_errors.append(f"Failed to click tab '{tab}': {e}")
                    
        except Exception as e:
            console_errors.append(f"Navigation/Execution Error: {str(e)}")
            
        await browser.close()
        
    print(f"E2E Crawl Complete. Writing report...")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# E2E Playwright Crawler Report\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## 1. Network 500 Errors\n")
        if not failed_requests:
            f.write("✅ No server errors detected.\n\n")
        else:
            for req in failed_requests:
                f.write(f"- ❌ {req}\n")
            f.write("\n")
            
        f.write("## 2. Browser Console Errors\n")
        if not console_errors:
            f.write("✅ No UI/JavaScript errors detected.\n\n")
        else:
            for err in console_errors:
                f.write(f"- ❌ `{err}`\n")
            f.write("\n")

if __name__ == "__main__":
    asyncio.run(run_e2e_crawler())
