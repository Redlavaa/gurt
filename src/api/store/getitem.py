import discord
import time
from curl_cffi.requests import AsyncSession

async def getitem(id: int):
    async with AsyncSession(impersonate="chrome") as s:
        start_time = time.perf_counter()
        
        try:
            url = f"https://api.polytoria.com/v1/store/{id}"
            response = await s.get(url, timeout=10)
            data = response.json()

            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            name = data.get("name") # use the () cause python is weird af
            id = data.get("id")
            icon = data.get("thumbnail")
            price = data.get("price")
            description = data.get("description")
            creator_name = data["creator"]["name"]


            embed = discord.Embed(
                title=name,
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=icon)
            embed.set_footer(text=f"Execution Time: {execution_time}ms")
            embed.add_field(
                name="Info",
                value=f"Creator: [{creator_name}](https://polytoria.com/u/{creator_name})\nID: {id}\nPrice: {price}\n", # manually does the url thing cause idgaf
                inline=False
            )
            embed.add_field(
                name="Description",
                value=description,
                inline=False
            )

            return embed

        except Exception as e:
            print(f"Error: {e}")
            return None