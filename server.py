import asyncio
import logging
import websockets
import names
import aiohttp

from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from main import fetch_exchange_rates  # Додайте імпорт

logging.basicConfig(level=logging.INFO)

class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = "Anonymous"
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            for client in self.clients:
                await client.send(message)

    async def handle_command(self, ws: WebSocketServerProtocol, command: str):
        parts = command.split()
        if parts[0] == "exchange":
            try:
                days = int(parts[1])
                exchange_rates = await fetch_exchange_rates(["USD", "EUR"], days)
                response = self.format_exchange_rates(exchange_rates)
                await self.send_to_clients(response)
            except (IndexError, ValueError):
                await ws.send("Invalid command. Usage: exchange <days>")

    async def ws_handler(self, ws: WebSocketServerProtocol, path: str):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            await self.handle_command(ws, message)

    def format_exchange_rates(self, exchange_rates):
        result = "Exchange Rates:\n"
        for date, rates in exchange_rates.items():
            result += f"{date} - USD: {rates['USD']}, EUR: {rates['EUR']}\n"
        return result


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
