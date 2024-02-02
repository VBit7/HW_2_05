import asyncio
import aiohttp
from datetime import datetime, timedelta

BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates"


async def fetch_exchange_rate(session, fetch_date):
    async with session.get(f"{BASE_URL}?date={fetch_date}") as response:
        text_json = await response.text()
        return text_json


async def fetch_exchange_rates():
    days_for_rate = 5
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_for_rate - 1)
    print(start_date.strftime("%d.%m.%Y"), end_date.strftime("%d.%m.%Y"))

    async with aiohttp.ClientSession() as session:
        tasks = []
        current_date = start_date
        while current_date <= end_date:
            tasks.append(fetch_exchange_rate(session, current_date.strftime("%d.%m.%Y")))
            current_date += timedelta(days=1)

        res = await asyncio.gather(*tasks)

    print(res)


async def main():
    await fetch_exchange_rates()

if __name__ == '__main__':
    asyncio.run(main())