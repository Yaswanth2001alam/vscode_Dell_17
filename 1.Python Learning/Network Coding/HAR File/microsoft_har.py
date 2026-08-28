import asyncio
from playwright.async_api import async_playwright


async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=False
        )

        context = await browser.new_context(
            record_har_path="microsoft.har"
        )

        page = await context.new_page()

        print("Opening Microsoft...")

        await page.goto(
            "https://www.microsoft.com",
            wait_until="networkidle"
        )

        print("Page title:", await page.title())

        await page.wait_for_timeout(5000)

        await context.close()
        await browser.close()

        print("HAR saved successfully: microsoft.har")


if __name__ == "__main__":
    asyncio.run(main())