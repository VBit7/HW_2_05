import asyncio
import aiofile
import logging
from datetime import datetime
from typing import List, Dict, Union, Tuple
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
import websockets
from main import fetch_exchange_rates


logging.basicConfig(level=logging.INFO)


class Server:
    clients: set[WebSocketServerProtocol] = set()

    async def register(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol) -> None:
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol) -> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol) -> None:
        async for message in ws:
            await self.handle_message(message)

    async def handle_message(self, message: str) -> None:
        if message.startswith("exchange"):
            parts = message.split()
            if len(parts) == 1:
                exchange_rates = await fetch_exchange_rates(["USD", "EUR"], 10)
                await self.send_to_clients(self.format_exchange_rates(exchange_rates))
            else:
                try:
                    days = min(int(parts[1]), 10)  # Maximum 10 days
                    currencies = ["USD", "EUR"]  # Default currencies
                    exchange_rates = await fetch_exchange_rates(currencies, days)
                    await self.send_to_clients(self.format_exchange_rates(exchange_rates))
                except ValueError:
                    await self.send_to_clients("Please provide a valid number of days for exchange rates.")

            async with aiofile.async_open("exchange_logs.txt", mode="a") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await f.write(f"{timestamp}: Executed exchange command\n")

    @staticmethod
    def format_exchange_rates(exchange_rates) -> str:
        formatted_rates = ""
        for date, rates in exchange_rates:
            formatted_rates += f"{date}\n"
            for currency, values in rates.items():
                formatted_rates += f"{currency}: Purchase Rate - {values['purchase_rate']}, Sale Rate - {values['sale_rate']}\n"
        return formatted_rates


async def main() -> None:
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
