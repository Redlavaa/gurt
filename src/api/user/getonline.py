from playwright.async_api import async_playwright
import json
import time
import discord
import asyncio
import re

# I dont know how to do this without playwright and it needs to be rewritten to use curl-cffi
# if anyone wants to fix it pls do 

async def getonline():
    async with async_playwright() as p:
        start_time = time.perf_counter()
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        try:
            await page.goto(f"https://polytoria.com/users/global", wait_until="domcontentloaded", timeout=100000)

            locator = page.locator('div[class="row small my-1"]')

            all_texts = await locator.all_inner_texts()
            multiline_string = all_texts[0]

            lines = multiline_string.splitlines()

            cleaned_lines = [
                int(re.sub(r'\D', '', line)) 
                for line in lines if any(char.isdigit() for char in line)
            ]

            ingame, online, total = cleaned_lines
            
            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            embed = discord.Embed(
            title="Online Players",
            color=discord.Color.blue()
            )

            embed.add_field(name="In Game", value=ingame, inline=True)
            embed.add_field(name="Online", value=online, inline=True)
            embed.set_footer(text=f"Execution Time: {execution_time} ms")

            return(embed, execution_time)

        finally:
            await page.close()