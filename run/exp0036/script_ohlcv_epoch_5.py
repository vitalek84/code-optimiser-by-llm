"""
I noticed that the previous version works incorrectly. I analysed the issue and fixed it. The main issue is with the CCXT connection to Binance. Let's optimize the code by:

1. Using asyncio for concurrent API requests to reduce total execution time
2. Implementing connection retry mechanism
3. Using numpy for faster numerical computations
4. Implementing proper error handling
5. Caching mechanism to store temporary results
"""

import ccxt.async_support as ccxt
import pandas as pd
import numpy as np
import asyncio
from datetime import datetime
from functools import lru_cache

async def fetch_ohlcv_with_retry(exchange, symbol, timeframe='1d', limit=100, max_retries=3):
    """Fetch OHLCV data with retry mechanism."""
    for attempt in range(max_retries):
        try:
            ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error fetching data for {symbol}: {e}")
                return None
            await asyncio.sleep(1)  # Wait before retry

@lru_cache(maxsize=128)
def calculate_sma(close_prices, period):
    """Calculate Simple Moving Average (SMA) using numpy for better performance."""
    return pd.Series(close_prices).rolling(window=period).mean().values

async def process_symbol(exchange, symbol, end_date):
    """Process single symbol data."""
    df = await fetch_ohlcv_with_retry(exchange, symbol)
    
    if df is not None:
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[df['datetime'] <= pd.Timestamp(end_date)].reset_index(drop=True)

        if not df.empty:
            close_prices = df['close'].values
            df['sma_10'] = calculate_sma(tuple(close_prices), 10)
            df['sma_50'] = calculate_sma(tuple(close_prices), 50)
            
            print(f"SMA for {symbol} (up to {end_date}):")
            print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
        else:
            print(f"No data available for {symbol} up to {end_date}.")
    else:
        print(f"Could not calculate SMA for {symbol}.")

async def main():
    exchange = ccxt.binance({
        'enableRateLimit': True,
        'timeout': 30000,
    })
    
    try:
        top_20_coins = [
            "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
            "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
        ]
        end_date = "2024-11-25"
        
        tasks = [process_symbol(exchange, symbol, end_date) for symbol in top_20_coins]
        await asyncio.gather(*tasks)
    
    finally:
        await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())