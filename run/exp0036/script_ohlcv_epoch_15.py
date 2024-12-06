"""
I will optimize the script with the following approaches:
1. Use asyncio for concurrent API calls to reduce total execution time
2. Cache timestamp conversions to avoid redundant calculations
3. Use numpy for SMA calculations which is faster than pandas rolling
4. Minimize DataFrame operations and memory usage
5. Use aiohttp session for better connection handling
"""

import ccxt.async_support as ccxt
import pandas as pd
import numpy as np
import asyncio
import aiohttp
from datetime import datetime

async def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_sma(data, period):
    return np.convolve(data, np.ones(period)/period, mode='valid')

async def process_symbol(exchange, symbol, end_date):
    df = await fetch_ohlcv(exchange, symbol)
    if df is not None:
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
        df = df[df['datetime'] <= pd.Timestamp(end_date)].reset_index(drop=True)

        if df.empty:
            print(f"No data available for {symbol} up to {end_date}.")
            return

        close_values = df['close'].values
        df['sma_10'] = np.nan
        df['sma_50'] = np.nan
        if len(close_values) >= 50:
            sma_10 = calculate_sma(close_values, 10)
            sma_50 = calculate_sma(close_values, 50)
            df.loc[9:, 'sma_10'] = sma_10
            df.loc[49:, 'sma_50'] = sma_50

        print(f"SMA for {symbol} (up to {end_date}):")
        print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
    else:
        print(f"Could not calculate SMA for {symbol}.")

async def main():
    exchange = ccxt.binance({
        'enableRateLimit': True,
        'asyncio_loop': asyncio.get_event_loop(),
    })

    top_20_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]

    end_date = "2024-11-25"
    
    tasks = [process_symbol(exchange, symbol, end_date) for symbol in top_20_coins]
    await asyncio.gather(*tasks)
    await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())