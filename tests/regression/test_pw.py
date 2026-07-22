import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating to ncloud...")
        await page.goto("https://www.ncloud.com/product/compute/gpuServer", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        
        # Extract text from the page
        text = await page.evaluate("document.body.innerText")
        with open("ncloud_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
            
        print("Navigating to sugarcube...")
        await page.goto("https://sugarcube.co.kr/v2/", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        text2 = await page.evaluate("document.body.innerText")
        with open("sugarcube_text.txt", "w", encoding="utf-8") as f:
            f.write(text2)
            
        await browser.close()

asyncio.run(run())
