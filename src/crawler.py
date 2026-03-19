import asyncio
import json
import time
from getplayer import get

async def start_crawling():
    print("Crawling")
    while True:
        with open("cache_ids.json", "r") as f:
            cache = json.load(f)
        ids_to_track = list(cache.keys()) 

        for user_id in ids_to_track:
            try:
                iduser = await get(user_id)
                print(f"Updated Profile(s) for {iduser}")
                
                await asyncio.sleep(5) 
                
            except Exception as e:
                print(f"Error crawling {iduser}: {e}")

        print("Waiting 1 minute...")
        await asyncio.sleep(60)
if __name__ == "__main__":
    asyncio.run(start_crawling())