import asyncio
import json
from pathlib import Path
from datetime import datetime, timedelta

from getplayer import get

CACHE_FILE = Path(__file__).resolve().parent / "cache_ids.json"

# Tracks the last time we successfully reached Polytoria in this process
last_polytoria_online: datetime | None = None


def _format_duration(delta: timedelta) -> str:
    """Return a human-readable duration like '3 minutes and 5 seconds'."""
    total_seconds = int(delta.total_seconds())
    if total_seconds <= 0:
        return "0 seconds"

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    parts: list[str] = []
    if days:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds and not parts:
        # Only show seconds if it's the only unit (for short outages)
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    if not parts:
        return "0 seconds"
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + f" and {parts[-1]}"


async def start_crawling():
    print("Crawling")
    while True:
        # Load IDs to track from the cache file located next to this script
        with CACHE_FILE.open("r", encoding="utf-8") as f:
            cache = json.load(f)

        ids_to_track = list(cache.keys())

        any_success = False

        for user_id in ids_to_track:
            try:
                # get(...) returns multiple values; we only need the name here
                name, *_ = await get(user_id)
                # Mark Polytoria as online on any successful request
                global last_polytoria_online
                last_polytoria_online = datetime.utcnow()
                any_success = True
                print(f"Updated profile for {name} (id {user_id})")

                await asyncio.sleep(5)

            except Exception as e:
                # Use user_id instead of possibly-unset local variables
                print(f"Error crawling user id {user_id}: {e}")

        # If we had no successful calls this round but had some in the past,
        # report how long it's been since Polytoria was last online.
        if not any_success and last_polytoria_online is not None:
            downtime = datetime.utcnow() - last_polytoria_online
            human_downtime = _format_duration(downtime)
            print(
                f"Looks like Polytoria is down! "
                f"{human_downtime} since Polytoria was last online"
            )

        print("Waiting 1 minute...")
        await asyncio.sleep(60)
if __name__ == "__main__":
    asyncio.run(start_crawling())