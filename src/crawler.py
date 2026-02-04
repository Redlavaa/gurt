import asyncio
import json
import time
from getplayer import get

async def start_crawling():
    print("Crawling")
    while True:
        with open("cache_profile.json", "rw") as f:
            cache = json.load(f)
        ids_to_track = ["1", "2", "3"] 

        for user_id in ids_to_track:
            try:
                name, networth, icon, exec_time = await get(user_id)
                print(f"Updated Profile(s)")
                
                await asyncio.sleep(5) 
                
            except Exception as e:
                print(f"Error crawling {user_id}: {e}")

        print("waiting 1 minute...")
        await asyncio.sleep(60)
if __name__ == "__main__":
    asyncio.run(start_crawling())