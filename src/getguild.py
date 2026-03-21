from playwright.async_api import async_playwright
import json
import time
import discord

async def getguild(id):
    async with async_playwright() as p:
        start_time = time.perf_counter()
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        try:
            await page.goto(f"https://api.polytoria.com/v1/guilds/{id}", wait_until="networkidle", timeout=100000)

            raw_text = await page.inner_text("body")
            data = json.loads(raw_text)

            name = data["name"]
            description = data["description"] if data["description"] else None
            creator = data["name"]
            id = data["id"]
            thumbnail = data["thumbnail"]
            
            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            if description == "":
                description == "None"

            embed = discord.Embed(
            title=f"{name} Info",
            color=discord.Color.blue()
            )

            embed.set_thumbnail(url=thumbnail)
            embed.add_field(name="Description", value=description, inline=True)
            embed.add_field(name="Creator", value=f"Username: {creator}\nId: {id}", inline=True)
            embed.set_footer(text=f"Execution Time: {execution_time} ms")

            return(embed)

        finally:
            await page.close()