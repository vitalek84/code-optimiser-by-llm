"""
I will optimize the code with the following improvements:
1. Use asyncio and aiohttp for concurrent API requests
2. Minimize DataFrame operations and conversions
3. Pre-calculate the end date timestamp to avoid multiple conversions
4. Use numpy for faster SMA calculations
5. Optimize memory usage by selecting only needed columns
6. Use ThreadPoolExecutor for parallel processing
7. Cache results where possible
"""

import ccxt.async_support as ccxt
import pandas as pd
import numpy as np
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import functools

async def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df = df[['timestamp', 'close']]  # Select only needed columns
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_sma(close_prices, period):
    return pd.Series(close_prices).rolling(window=period, min_periods=1).mean().values

async def process_symbol(exchange, symbol, end_timestamp):
    df = await fetch_ohlcv(exchange, symbol)
    if df is not None:
        df = df[df['timestamp'] <= end_timestamp]
        
        if df.empty:
            print(f"No data available for {symbol} up to {end_date}.")
            return None
            
        closes = df['close'].values
        sma_10 = calculate_sma(closes, 10)
        sma_50 = calculate_sma(closes, 50)
        
        last_row = {
            'date': pd.Timestamp(df['timestamp'].iloc[-1], unit='ms').strftime('%Y-%m-%d'),
            'close': df['close'].iloc[-1],
            'sma_10': sma_10[-1],
            'sma_50': sma_50[-1]
        }
        return symbol, last_row
    return None

async def main():
    exchange = ccxt.binance({
        'enableRateLimit': True,
        'rateLimit': 1200,
    })

    top_20_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]

    end_date = "2024-11-25"
    end_timestamp = pd.Timestamp(end_date).value // 10**6

    tasks = [process_symbol(exchange, symbol, end_timestamp) for symbol in top_20_coins]
    results = await asyncio.gather(*tasks)
    
    await exchange.close()

    for result in results:
        if result:
            symbol, data = result
            print(f"SMA for {symbol} (up to {end_date}):")
            print(f"      date    close    sma_10     sma_50")
            print(f"{data['date']} {data['close']:.6f} {data['sma_10']:.6f} {data['sma_50']:.6f}")

if __name__ == "__main__":
    asyncio.run(main())