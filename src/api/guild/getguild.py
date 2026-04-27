import discord
import time
from curl_cffi.requests import AsyncSession

async def getguild(id):
    async with AsyncSession(impersonate="chrome") as s:
        start_time = time.perf_counter()
        
        try:
            url = f"https://api.polytoria.com/v1/guilds/{id}"
            response = await s.get(url, timeout=10)
            data = response.json()

            name = data["name"]
            description = data["description"] if data["description"] else None # im not sure what this error checking is for but im just gonna keep it
            creator = data["name"]
            id = data["id"]
            thumbnail = data["thumbnail"]
            
            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            if description == "": # if the description is empty set it to none
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

        except Exception as e:
            print(f"Error: {e}")
            return None