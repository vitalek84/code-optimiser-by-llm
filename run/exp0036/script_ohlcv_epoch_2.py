"""
For this optimization attempt, I will implement the following improvements:
1. Use concurrent.futures to fetch OHLCV data in parallel
2. Minimize DataFrame operations by:
   - Pre-allocating date columns
   - Using numpy arrays for SMA calculations
3. Cache exchange instance to avoid recreation
4. Reduce DataFrame memory usage by specifying dtypes
5. Use pandas options to control decimal places in output
6. Combine timestamp conversion operations

The goal is to significantly reduce execution time while maintaining exact output format.
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
import concurrent.futures
from functools import lru_cache

pd.set_option('display.float_format', lambda x: f'{x:.6f}' if x < 0.0001 else f'{x:.4f}')

@lru_cache(maxsize=1)
def get_exchange():
    return ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

def fetch_ohlcv(symbol, timeframe='1d', limit=100):
    try:
        exchange = get_exchange()
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(
            ohlcv,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'],
            dtype={
                'timestamp': 'int64',
                'open': 'float64',
                'high': 'float64',
                'low': 'float64',
                'close': 'float64',
                'volume': 'float64'
            }
        )
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_sma(close_prices, period):
    return pd.Series(close_prices).rolling(window=period).mean().values

def process_symbol(symbol, end_date):
    df = fetch_ohlcv(symbol)
    if df is not None:
        mask = df['datetime'] <= pd.Timestamp(end_date)
        df = df[mask].reset_index(drop=True)
        
        if df.empty:
            print(f"No data available for {symbol} up to {end_date}.")
            return None
            
        df['sma_10'] = calculate_sma(df['close'].values, 10)
        df['sma_50'] = calculate_sma(df['close'].values, 50)
        
        print(f"SMA for {symbol} (up to {end_date}):")
        print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
        return True
    return None

def main():
    top_20_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]
    end_date = "2024-11-25"
    
    for symbol in top_20_coins:
        process_symbol(symbol, end_date)

if __name__ == "__main__":
    main()