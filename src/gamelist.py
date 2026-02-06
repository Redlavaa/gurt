from playwright.async_api import async_playwright
import json
import time
import discord

async def list():
    async with async_playwright() as p:
        start_time = time.perf_counter()
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()

        try:
            await page.goto(f"https://polytoria.com/api/places", wait_until="domcontentloaded", timeout=1000000)

            raw_text = await page.inner_text("body")
            data = json.loads(raw_text)

            names = []
            ids = []
            players = []

            top = data["data"][:5]

            for item in top:
                names.append(item["name"])
                ids.append(str(item["id"]))

            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            embed = discord.Embed(
            title="Game List",
            color=discord.Color.blue()
        )
            
            for i in range(len(names)):
                embed.add_field(
                    name=f"{names[i]}",
                    value=f"[{names[i]}](https://polytoria.com/places/{ids[i]})",
                    inline=False
                )
                embed.set_footer(text=f"Execution Time: {execution_time} ms")

            return(names, ids, execution_time, embed)

        finally:
            await page.close()