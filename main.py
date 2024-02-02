import aiohttp
import asyncio
from datetime import datetime, timedelta

class PrivatBankAPI:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates"

    @staticmethod
    async def get_exchange_rate(session, currency, date):
        params = {"json": "", "date": date.strftime("%d.%m.%Y")}
        async with session.get(f"{PrivatBankAPI.BASE_URL}?exchange&coursid=5", params=params) as response:
            data = await response.json()
            rates = data.get("exchangeRate")
            for rate in rates:
                if rate["currency"] == currency:
                    return rate["purchaseRateNB"], rate["saleRateNB"]
        return None

async def fetch_exchange_rates():
    currencies = ["USD", "EUR"]
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10)

    async with aiohttp.ClientSession() as session:
        for currency in currencies:
            print(f"Exchange rates for {currency} in the last 10 days:")
            current_date = start_date
            while current_date <= end_date:
                try:
                    purchase_rate, sale_rate = await PrivatBankAPI.get_exchange_rate(session, currency, current_date)
                    print(f"{current_date.strftime('%Y-%m-%d')}: Purchase Rate - {purchase_rate}, Sale Rate - {sale_rate}")
                except Exception as e:
                    print(f"Error fetching exchange rates for {currency} on {current_date.strftime('%Y-%m-%d')}: {e}")

                current_date += timedelta(days=1)

async def main():
    await fetch_exchange_rates()

if __name__ == "__main__":
    asyncio.run(main())





# # Version 1
# import aiohttp
# import asyncio
# from datetime import datetime, timedelta
#
# class PrivatBankAPI:
#     BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates"
#
#     @staticmethod
#     async def get_exchange_rate(currency, date):
#         async with aiohttp.ClientSession() as session:
#             params = {"json": "", "date": date.strftime("%d.%m.%Y")}
#             async with session.get(f"{PrivatBankAPI.BASE_URL}?exchange&coursid=5", params=params) as response:
#                 data = await response.json()
#                 rates = data.get("exchangeRate")
#                 for rate in rates:
#                     if rate["currency"] == currency:
#                         return rate["purchaseRateNB"], rate["saleRateNB"]
#         return None
#
# async def fetch_exchange_rates():
#     currencies = ["USD", "EUR"]
#     end_date = datetime.now()
#     start_date = end_date - timedelta(days=10)
#
#     for currency in currencies:
#         print(f"Exchange rates for {currency} in the last 10 days:")
#         current_date = start_date
#         while current_date <= end_date:
#             try:
#                 purchase_rate, sale_rate = await PrivatBankAPI.get_exchange_rate(currency, current_date)
#                 print(f"{current_date.strftime('%Y-%m-%d')}: Purchase Rate - {purchase_rate}, Sale Rate - {sale_rate}")
#             except Exception as e:
#                 print(f"Error fetching exchange rates for {currency} on {current_date.strftime('%Y-%m-%d')}: {e}")
#
#             current_date += timedelta(days=1)
#
# async def main():
#     await fetch_exchange_rates()
#
# if __name__ == "__main__":
#     asyncio.run(main())
