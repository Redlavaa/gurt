import asyncio
import json
from pathlib import Path

from getplayer import get

CACHE_FILE = Path(__file__).resolve().parent / "cache_ids.json"


async def start_crawling():
    print("Crawling")
    while True:
        # Load IDs to track from the cache file located next to this script
        with CACHE_FILE.open("r", encoding="utf-8") as f:
            cache = json.load(f)

        ids_to_track = list(cache.keys())

        for user_id in ids_to_track:
            try:
                # get(...) returns multiple values; we only need the name here
                name, *_ = await get(user_id)
                print(f"Updated profile for {name} (id {user_id})")

                await asyncio.sleep(5)

            except Exception as e:
                # Use user_id instead of possibly-unset local variables
                print(f"Error crawling user id {user_id}: {e}")

        print("Waiting 1 minute...")
        await asyncio.sleep(60)
if __name__ == "__main__":
    asyncio.run(start_crawling())