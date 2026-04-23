import discord
import time
from curl_cffi.requests import AsyncSession

async def list():
    async with AsyncSession(impersonate="chrome") as s:
        start_time = time.perf_counter()
        
        try:
            url = f"https://polytoria.com/api/places"
            response = await s.get(url, timeout=10)
            data = response.json()

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

            return(embed)

        except Exception as e:
            print(f"Error: {e}")
            return None