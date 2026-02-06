import asyncio
import json
import time
from getonline import getonline

async def start_crawling():
    print("Crawling")
    while True:
        with open("src\cache\cache_playercount.json", "r") as f:
            cache = json.load(f)

            getonline(update_cache=cache)
            f.seek(0)
            json.dump(cache, f, indent=4)

        print("waiting 1 minute...")
        await asyncio.sleep(60)
if __name__ == "__main__":
    asyncio.run(start_crawling())