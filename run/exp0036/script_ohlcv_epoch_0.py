"""
I will optimize the code by:
1. Using asyncio for concurrent API requests to reduce waiting time
2. Minimizing DataFrame operations by:
   - Combining timestamp conversions
   - Using numpy for SMA calculations
   - Reducing DataFrame copies
3. Caching date calculations
4. Pre-allocating DataFrames
5. Using more efficient data structures
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
    
def calculate_sma(closes, period):
    return pd.Series(closes).rolling(window=period, min_periods=1).mean().values

async def process_symbol(exchange, symbol, end_date_ts):
    df = await fetch_ohlcv(exchange, symbol)
    
    if df is not None:
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[df['datetime'] <= end_date_ts].reset_index(drop=True)
        
        if not df.empty:
            closes = df['close'].values
            df['sma_10'] = calculate_sma(closes, 10)
            df['sma_50'] = calculate_sma(closes, 50)
            df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
            
            last_row = df[['date', 'close', 'sma_10', 'sma_50']].iloc[-1]
            return symbol, last_row
    return symbol, None

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
    end_date_ts = pd.Timestamp(end_date)
    
    tasks = [process_symbol(exchange, symbol, end_date_ts) for symbol in top_20_coins]
    results = await asyncio.gather(*tasks)
    
    await exchange.close()
    
    for symbol, result in results:
        if result is not None:
            print(f"SMA for {symbol} (up to {end_date}):")
            print(result.to_frame().T.to_string(index=False))
        else:
            print(f"Could not calculate SMA for {symbol}.")

if __name__ == "__main__":
    asyncio.run(main())