from playwright.async_api import async_playwright
import json
import time


async def getuserid(username: str):
    async with async_playwright() as p:
        start_time = time.perf_counter()
        browser = None
        page = None

        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = await context.new_page()

            await page.goto(
                f"https://api.polytoria.com/v1/users/find?username={username}",
                wait_until="domcontentloaded",
                timeout=100000,
            )

            raw_text = await page.inner_text("body")
            data = json.loads(raw_text)

            user_id = data["id"]

            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            return user_id, execution_time

        finally:
            # Ensure page and browser are properly closed, even if creation failed
            if page is not None:
                await page.close()
            if browser is not None:
                await browser.close()