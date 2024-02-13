"""
Приклади використання:

1. Запуск без аргументів:
python main.py                  # Ця команда виконає код з налаштуваннями за замовчуванням
                                # (курс валют за останні 10 днів для валют USD та EUR).

2. Зміна кількості днів:
python main.py --days 5         # Змінить кількість днів, за якими буде виведений курс валют.
                                # У цьому випадку будуть відображені курси за останні 5 днів.

3. Зміна валют:
python main.py --currencies USD EUR GBP     # Змінить список валют, за якими буде виведений курс.
                                            # У цьому випадку будуть відображені курси для долара США (USD),
                                            # євро (EUR) та фунта стерлінгів (GBP).

4. Комбіноване використання аргументів:
python main.py --days 7 --currencies USD EUR        # У цьому випадку будуть відображені курси за останні 7 днів
                                                    # для долара США (USD) та євро (EUR).
"""
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
    result = []

    async with aiohttp.ClientSession() as session:
        current_date = start_date
        while current_date <= end_date:
            rates_for_date = {}
            for currency in currencies:
                date, purchase_rate, sale_rate = await fetch_exchange_rate(session, currency, current_date)
                rates_for_date[currency] = {"purchase_rate": purchase_rate, "sale_rate": sale_rate}
            result.append((current_date.strftime('%d-%m-%Y'), rates_for_date))
            current_date += timedelta(days=1)
    return result


def print_exchange_rates(exchange_rates):
    print(f"{'Date':<12}", end="")
    for currency in exchange_rates[0][1].keys():
        print(f"{currency} Purchase Rate\t{currency} Sale Rate\t", end="")
    print()

    for date, rates in exchange_rates:
        print(f"{date:<12}", end="")
        for currency, values in rates.items():
            print(f"{values['purchase_rate']:<20}{values['sale_rate']:<20}", end="")
        print()


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch exchange rates from PrivatBank API.")
    parser.add_argument("--days", type=int, default=10, help="Number of days to fetch exchange rates for.")
    parser.add_argument(
        "--currencies",
        nargs="+",
        default=["USD", "EUR"],
        choices=["USD", "EUR", "GBP", "CHF", "PLN", "CZK"],
        help="Currency codes to fetch."
    )
    return parser.parse_args()


async def main():
    args = parse_args()
    exchange_rates = await fetch_exchange_rates(args.currencies, args.days)
    print_exchange_rates(exchange_rates)

if __name__ == "__main__":
    asyncio.run(main())
