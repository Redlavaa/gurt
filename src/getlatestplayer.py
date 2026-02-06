import discord
from playwright.async_api import async_playwright
import json
import time

async def getlatest():
    async with async_playwright() as p:
        start_time = time.perf_counter()
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        try:
            await page.goto(f"https://api.polytoria.com/v1/users?sort=registeredAt&order=desc&limit=1", wait_until="domcontentloaded", timeout=100000)

            raw_text = await page.inner_text("body")
            data = json.loads(raw_text)
            
            name = data["users"][0]["username"]
            id = data["users"][0]["id"]
            icon = data["users"][0]["thumbnail"]["icon"]
            
            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            embed = discord.Embed(
            title=f"{name}'s Profile",
            color=discord.Color.blue()
        )
            embed.set_thumbnail(url=icon)
            embed.set_footer(text=f"Execution Time: {execution_time}ms")
            embed.add_field(
                name="Info",
                value=f"ID: {id}",
                inline=False
                )

            return(name, id, icon, execution_time, embed)
        finally:
            await page.close()