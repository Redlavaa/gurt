import discord
import time
from curl_cffi.requests import AsyncSession

async def download(id: int):
    async with AsyncSession(impersonate="chrome") as s:
        start_time = time.perf_counter()
        
        try:
            url = f"https://api.polytoria.com/v1/assets/serve/{id}/Asset"
            response = await s.get(url, timeout=10)
            data = response.json()

            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            url = data["url"]

            embed = discord.Embed(
                title=f"Download",
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Execution Time: {execution_time}ms")
            embed.add_field(
                name="Download Link",
                value=f"[Click here]({url})",
                inline=False
            )
            return (embed, execution_time)

        except Exception as e:
            print(f"Error: {e}")
            return None