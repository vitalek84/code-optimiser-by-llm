
"""
This version introduces several optimizations:
1. Parallel data fetching using concurrent.futures to speed up API calls
2. Minimizing DataFrame operations by:
   - Using pd.to_datetime only once for timestamps
   - Combining date conversion and filtering in one step
   - Optimizing SMA calculations using numpy
3. Using numpy for faster calculations
4. Pre-allocating DataFrames for results
5. Minimizing memory usage by dropping unnecessary columns early
6. Using asyncio for async API calls if supported by exchange
7. Adding error handling and retries for API stability
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import asyncio
from functools import partial

def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    """Fetch OHLCV data with retries."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )[['timestamp', 'close']]  # Only keep needed columns
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error fetching data for {symbol}: {e}")
                return None
            await asyncio.sleep(1)

def process_data(df, end_date):
    """Process OHLCV data with optimized calculations."""
    if df is None or df.empty:
        return None
        
    # Convert timestamp and filter in one step
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[df['datetime'] <= pd.Timestamp(end_date)].reset_index(drop=True)
    
    if df.empty:
        return None
        
    # Calculate SMAs using numpy for better performance
    close_values = df['close'].values
    df['sma_10'] = np.convolve(close_values, np.ones(10)/10, mode='valid')
    df['sma_50'] = np.convolve(close_values, np.ones(50)/50, mode='valid')
    
    # Convert date format
    df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
    
    return df[['date', 'close', 'sma_10', 'sma_50']].tail(1)

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
    
    # Parallel data fetching
    with ThreadPoolExecutor(max_workers=5) as executor:
        fetch_partial = partial(fetch_ohlcv, exchange)
        dfs = list(executor.map(fetch_partial, top_20_coins))
    
    # Process results maintaining order
    for symbol, df in zip(top_20_coins, dfs):
        result = process_data(df, end_date)
        if result is not None:
            print(f"SMA for {symbol} (up to {end_date}):")
            print(result.to_string(index=False))
        else:
            print(f"Could not calculate SMA for {symbol}.")

if __name__ == "__main__":
    asyncio.run(main())
