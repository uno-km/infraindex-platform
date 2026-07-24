import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://vessl.ai/ko/pricing", wait_until="networkidle")
        content = await page.evaluate("document.body.innerText")
        print(content[:1500])
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
