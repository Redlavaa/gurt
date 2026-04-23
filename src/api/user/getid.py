import discord
import time
from curl_cffi.requests import AsyncSession

async def getuserid(username: str):
    async with AsyncSession(impersonate="chrome") as s:
        start_time = time.perf_counter()
        
        try:
            url = f"https://api.polytoria.com/v1/users/find?username={username}"
            response = await s.get(url, timeout=10)
            data = response.json()

            end_time = time.perf_counter()
            execution_time = round((end_time - start_time) * 1000, 2)

            return (data["id"], execution_time)

        except Exception as e:
            print(f"Error: {e}")
            return None