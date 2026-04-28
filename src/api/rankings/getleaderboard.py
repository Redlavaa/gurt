import discord
import time
import json
from curl_cffi.requests import AsyncSession

async def getrankings(type: str, page: int):
    async with AsyncSession(impersonate="chrome") as s:
        start_time = time.perf_counter()
        
        try:
            url = f"https://api.polytoria.com/v1/rankings?category={type}&page={page}&limit=10"
            response = await s.get(url, timeout=10)
            data = response.json()

            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            leaderboard_list =[]

            for entry in data["data"]: # for each entry in the leaderboard add it to the list
                rank = entry["rank"]
                name = entry["user"]["username"]
                stat = entry["statistic"]

                row = f"{rank} - {name}: {stat}" # formats the data in a row
                leaderboard_list.append(row) # adds the row to the list

                leaderboard_display = "\n".join(leaderboard_list) # adds newlines between each row


            embed = discord.Embed(
                title=f"{type} Leaderboard",
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Execution Time: {execution_time}ms")
            embed.add_field(
                name="Rankings",
                value=leaderboard_display,
                inline=False
            )

            return embed

        except Exception as e:
            print(f"Error: {e}")
            return None