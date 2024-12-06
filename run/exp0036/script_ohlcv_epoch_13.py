"""
For this optimization attempt, I will focus on several key improvements:
1. Use concurrent.futures to parallelize API calls for different symbols
2. Precompute the end date timestamp to avoid repeated conversions
3. Use numpy for SMA calculations instead of pandas rolling
4. Minimize DataFrame operations by performing calculations on raw data
5. Use aiohttp and asyncio for async API calls
6. Reduce memory usage by selecting only needed columns early
7. Cache timestamp conversions
"""

import ccxt
import pandas as pd
import numpy as np
import asyncio
import aiohttp
from datetime import datetime
import concurrent.futures
from functools import lru_cache

@lru_cache(maxsize=128)
def convert_timestamp(ts):
    return pd.Timestamp(ts, unit='ms').strftime('%Y-%m-%d')

def calculate_sma_numpy(data, period):
    return np.convolve(data, np.ones(period)/period, mode='valid')

async def fetch_ohlcv_async(session, exchange, symbol, timeframe='1d', limit=100):
    try:
        ohlcv = await exchange.fetch_ohlcv_async(symbol, timeframe, limit=limit)
        if ohlcv:
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            return symbol, df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
    return symbol, None

async def process_symbol(exchange, symbol, end_timestamp):
    try:
        ohlcv = await exchange.fetch_ohlcv_async(symbol, '1d', limit=100)
        if not ohlcv:
            return symbol, None
        
        # Convert to numpy array for faster processing
        data = np.array(ohlcv)
        mask = data[:, 0] <= end_timestamp
        filtered_data = data[mask]
        
        if len(filtered_data) == 0:
            return symbol, None
            
        close_prices = filtered_data[:, 4]
        timestamps = filtered_data[:, 0]
        
        # Calculate SMAs using numpy
        if len(close_prices) >= 50:
            sma_10 = calculate_sma_numpy(close_prices, 10)[-1]
            sma_50 = calculate_sma_numpy(close_prices, 50)[-1]
            
            result = {
                'date': convert_timestamp(timestamps[-1]),
                'close': close_prices[-1],
                'sma_10': sma_10,
                'sma_50': sma_50
            }
            return symbol, result
    except Exception as e:
        print(f"Error processing {symbol}: {e}")
    return symbol, None

async def main():
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
        'asyncio_loop': asyncio.get_event_loop(),
    })
    
    if not hasattr(exchange, 'fetch_ohlcv_async'):
        exchange.fetch_ohlcv_async = exchange.fetch_ohlcv
    
    top_20_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]
    
    end_date = "2024-11-25"
    end_timestamp = pd.Timestamp(end_date).value // 10**6

    tasks = [process_symbol(exchange, symbol, end_timestamp) for symbol in top_20_coins]
    results = await asyncio.gather(*tasks)
    
    results_dict = dict(results)
    
    for symbol in top_20_coins:
        result = results_dict.get(symbol)
        if result:
            print(f"SMA for {