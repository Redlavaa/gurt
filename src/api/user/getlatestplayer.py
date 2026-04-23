import discord
import time
from curl_cffi.requests import AsyncSession

async def getlatest():
    async with AsyncSession(impersonate="chrome") as s:
        start_time = time.perf_counter()
        
        try:
            url = f"https://api.polytoria.com/v1/users?sort=registeredAt&order=desc&limit=1"
            response = await s.get(url, timeout=10)
            data = response.json()

            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            name = data["users"][0]["username"]
            id = data["users"][0]["id"]
            icon = data["users"][0]["thumbnail"]["icon"]


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

            return (embed, execution_time)

        except Exception as e:
            print(f"Error: {e}")
            return None