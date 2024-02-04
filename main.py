import aiohttp
import asyncio
from datetime import datetime, timedelta
import argparse

class PrivatBankAPI:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates"

    @staticmethod
    async def get_exchange_rate(session, date):
        params = {"json": "", "date": date.strftime("%d.%m.%Y")}
        async with session.get(PrivatBankAPI.BASE_URL, params=params) as response:
            data = await response.json()
            rates = data.get("exchangeRate")
            return rates

async def fetch_exchange_rate(session, currency, current_date):
    exchange_rates = await PrivatBankAPI.get_exchange_rate(session, current_date)
    for rate in exchange_rates:
        if rate["baseCurrency"] == "UAH" and rate["currency"] == currency:
            return current_date.strftime('%Y-%m-%d'), rate.get("purchaseRate"), rate.get("saleRate")
    return current_date.strftime('%Y-%m-%d'), None, None

async def fetch_exchange_rates(currencies, days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days - 1)

    async with aiohttp.ClientSession() as session:
        print(f"{'Date':<12}", end="")
        for currency in currencies:
            print(f"{currency} Purchase Rate\t{currency} Sale Rate\t", end="")
        print()

        current_date = start_date
        while current_date <= end_date:
            print(f"{current_date.strftime('%d-%m-%Y'):<12}", end="")
            for currency in currencies:
                date, purchase_rate, sale_rate = await fetch_exchange_rate(session, currency, current_date)
                print(f"{purchase_rate:<20}{sale_rate:<20}", end="")
            print()
            current_date += timedelta(days=1)

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch exchange rates from PrivatBank API.")
    parser.add_argument("--days", type=int, default=10, help="Number of days to fetch exchange rates for.")
    parser.add_argument("--currencies", nargs="+", default=["USD", "EUR"], choices=["USD", "EUR", "GBP", "CHF", "PLN", "CZK"], help="Currency codes to fetch.")
    return parser.parse_args()

async def main():
    args = parse_args()
    await fetch_exchange_rates(args.currencies, args.days)

if __name__ == "__main__":
    asyncio.run(main())
