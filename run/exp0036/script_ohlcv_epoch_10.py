"""
I plan to optimize the code in the following ways:
1. Implement async/await pattern for fetching data as most time is spent on I/O operations
2. Use NumPy for calculations instead of pandas where possible
3. Precompute pd.Timestamp(end_date) to avoid redundant conversions
4. Use pandas more efficiently by avoiding redundant operations
5. Format output to match exactly the reference results order
6. I noticed that the results order in previous version was incorrect compared to reference results, will fix that
"""

import ccxt.async_support as ccxt
import pandas as pd
import numpy as np
import asyncio
from datetime import datetime

async def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def process_data(df, end_date_ts):
    if df is None:
        return None
    
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[df['datetime'] <= end_date_ts].reset_index(drop=True)
    
    if df.empty:
        return None
        
    df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
    close_values = df['close'].values
    df['sma_10'] = pd.Series(np.convolve(close_values, np.ones(10)/10, mode='valid'), index=df.index[9:])
    df['sma_50'] = pd.Series(np.convolve(close_values, np.ones(50)/50, mode='valid'), index=df.index[49:])
    
    return df[['date', 'close', 'sma_10', 'sma_50']].tail(1)

async def main():
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })
    
    try:
        top_20_coins = [
            "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
            "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
        ]

        end_date_ts = pd.Timestamp("2024-11-25")
        
        tasks = [fetch_ohlcv(exchange, symbol) for symbol in top_20_coins]
        results = await asyncio.gather(*tasks)
        
        for symbol, df in zip(top_20_coins, results):
            result_df = process_data(df, end_date_ts)
            if result_df is not None:
                print(f"SMA for {symbol} (up to 2024-11-25):")
                print(result_df.to_string(index=False))
            else:
                print(f"Could not calculate SMA for {symbol}.")
                
    finally:
        await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())