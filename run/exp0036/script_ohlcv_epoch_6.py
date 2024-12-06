"""
Chain of thought for optimization:
1. The main bottleneck in this script is the sequential API calls to fetch_ohlcv
2. We can parallelize these calls using asyncio and aiohttp
3. CCXT provides async support through ccxt.async_support
4. We'll batch process the dataframe operations
5. We'll reduce memory usage by only keeping necessary columns
6. We'll optimize pandas operations by pre-allocating memory where possible
7. We'll use numpy for faster calculations
"""

import ccxt.async_support as ccxt
import pandas as pd
import numpy as np
import asyncio
from datetime import datetime

async def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df[['date', 'datetime', 'close']]
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_smas(df):
    close_array = df['close'].to_numpy()
    sma_10 = pd.Series(np.convolve(close_array, np.ones(10)/10, mode='valid')).shift(9)
    sma_50 = pd.Series(np.convolve(close_array, np.ones(50)/50, mode='valid')).shift(49)
    return sma_10, sma_50

async def process_symbol(exchange, symbol, end_date):
    df = await fetch_ohlcv(exchange, symbol)
    if df is not None:
        df = df[df['datetime'] <= pd.Timestamp(end_date)].reset_index(drop=True)
        if not df.empty:
            sma_10, sma_50 = calculate_smas(df)
            df['sma_10'] = sma_10
            df['sma_50'] = sma_50
            result = df[['date', 'close', 'sma_10', 'sma_50']].tail(1)
            print(f"SMA for {symbol} (up to {end_date}):")
            print(result.to_string(index=False))
        else:
            print(f"No data available for {symbol} up to {end_date}.")
    else:
        print(f"Could not calculate SMA for {symbol}.")
    return symbol

async def main():
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
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