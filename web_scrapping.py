import asyncio
import aiohttp
from datetime import datetime
import csv
import pandas as pd
import os
import sys
sys.setrecursionlimit('100000')


async def get_crypto_price(session, crypto):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={crypto}USDT"
    async with session.get(url) as response:
        return await response.json()


async def main():
    fieldnames = ["time", "BTC", "ETH", "BNB", "SOL", "ADA", "DOT"]
    if not os.path.isfile("crypto_prices.csv"):
        with open("crypto_prices.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    df = pd.DataFrame(columns=fieldnames)
    async with aiohttp.ClientSession() as session:
        crypto_prices = await asyncio.gather(
            get_crypto_price(session, "BTC"),
            get_crypto_price(session, "ETH"),
            get_crypto_price(session, "BNB"),
            get_crypto_price(session, "SOL"),
            get_crypto_price(session, "ADA"),
            get_crypto_price(session, "DOT"),
        )
        crypto_prices = dict(zip(["BTC", "ETH", "BNB", "SOL", "ADA", "DOT"], crypto_prices))
        cryptos = {'time': datetime.now().strftime("%H:%M:%S")}
        for crypto in crypto_prices:
            cryptos[f'{crypto}'] = crypto_prices[crypto]['price']
        df = df.append(cryptos, ignore_index=True)
        df.to_csv("crypto_prices.csv", mode='a', header=False)
    for i in range(60*24*30):
        await asyncio.sleep(2)
        await main()

asyncio.run(main())

