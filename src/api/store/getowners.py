import discord
import time
import json
from curl_cffi.requests import AsyncSession

async def getowners(id: int ,page: int):
    async with AsyncSession(impersonate="chrome") as s:
        start_time = time.perf_counter()
        
        try:
            url = f"https://api.polytoria.com/v1/store/{id}/owners?page={page}&limit=10"
            response = await s.get(url, timeout=10)
            data = response.json()

            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            owners_list = []

            for entry in data["data"]: # for each entry in the leaderboard add it to the list
                serial = entry["serial"]
                name = entry["user"]["username"]

                row = f"{serial} - ({name})[https://polytoria.com/u/{name}]" # formats the data in a row
                owners_list.append(row) # adds the row to the list

                owners_display = "\n".join(owners_list) # adds newlines between each row


            embed = discord.Embed(
                title=f"{id} Owners",
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Execution Time: {execution_time}ms")
            embed.add_field(
                name="Owners",
                value=owners_display,
                inline=False
            )

            return embed

        except Exception as e:
            print(f"Error: {e}")
            return None