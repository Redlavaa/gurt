import discord
import time
from curl_cffi.requests import AsyncSession

async def getgame(id: int):
    async with AsyncSession(impersonate="chrome") as s:
        start_time = time.perf_counter()
        
        try:
            url = f"https://api.polytoria.com/v1/places/{id}"
            response = await s.get(url, timeout=10)
            data = response.json()

            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            name = data.get("name")
            description = data.get("description")
            icon = data.get("thumbnail")
            visits = data.get("visits")
            playercount = data.get("playing")
            creator = data["creator"]["name"]


            embed = discord.Embed(
                title=f"{name}",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=icon)
            embed.set_footer(text=f"Execution Time: {execution_time}ms")
            embed.add_field(
                name="Info",
                value=f"Creator: {creator}\nVisits: {visits}\nPlaying: {playercount}",
                inline=False
                )
            embed.add_field(
                name="Description",
                value=f"{description}",
                inline=False
                )

            return (embed, execution_time)

        except Exception as e:
            print(f"Error: {e}")
            return None