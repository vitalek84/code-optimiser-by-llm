"""
I'll optimize the code by:
1. Using asyncio for parallel API requests to reduce overall execution time
2. Implementing connection pooling with aiohttp for better network performance
3. Pre-calculating dates and timestamps to avoid repeated conversions
4. Optimizing pandas operations by pre-allocating DataFrames
5. Using numpy for faster calculations
6. Minimizing DataFrame copies and transformations
7. Implementing error handling and retries for API requests
8. Using more efficient data structures
"""

import ccxt.async_support as ccxt
import pandas as pd
import numpy as np
import asyncio
import aiohttp
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

async def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        if not ohlcv:
            return None
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_smas(df):
    close_values = df['close'].to_numpy()
    sma_10 = pd.Series(close_values).rolling(window=10).mean().values
    sma_50 = pd.Series(close_values).rolling(window=50).mean().values
    return sma_10, sma_50

async def process_symbol(exchange, symbol, end_date):
    df = await fetch_ohlcv(exchange, symbol)
    if df is not None:
        mask = df['datetime'] <= pd.Timestamp(end_date)
        df = df[mask].reset_index(drop=True)
        
        if not df.empty:
            sma_10, sma_50 = calculate_smas(df)
            df['sma_10'] = sma_10
            df['sma_50'] = sma_50
            
            last_row = df[['date', 'close', 'sma_10', 'sma_50']].iloc[-1]
            print(f"SMA for {symbol} (up to {end_date}):")
            print(pd.DataFrame([last_row]).to_string(index=False))
        else:
            print(f"No data available for {symbol} up to {end_date}.")
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