import discord
import json
import time
from curl_cffi.requests import AsyncSession

async def get(id):
    async with AsyncSession(impersonate="chrome") as s:
        start_time = time.perf_counter()
        
        try:
            url = f"https://api.polytoria.com/v1/users/{id}"
            response = await s.get(url, timeout=10)
            data = response.json()


            name = data["username"]
            networth = data["netWorth"]
            membership = data["membershipType"]
            placevisits = data["placeVisits"]
            icon = data["thumbnail"]["icon"]
            staff = data["isStaff"]

            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            if staff == True:
                embedcolor = discord.Color.red
            elif membership == 'plusDeluxe':
                embedcolor = discord.Color.purple
            elif membership == 'plus':
                embedcolor = discord.Color.teal
            else:
                embedcolor = discord.Color.light_grey

            embed = discord.Embed(
                title=f"{name}'s Profile",
                color=embedcolor()
            )
            embed.set_thumbnail(url=icon)
            embed.set_footer(text=f"Execution Time: {execution_time}ms")
            embed.add_field(
                name="Networth",
                value=f"Networth: {networth}",
                inline=False
                )
            embed.add_field(
                name="Place visits",
                value=f"Place Visits: {placevisits}",
                inline=False
            )

            return (embed, execution_time)

        except Exception as e:
            print(f"Error: {e}")
            return None