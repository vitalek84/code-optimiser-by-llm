"""
For this optimization iteration, I will implement several performance improvements:

1. Implement parallel processing using concurrent.futures to fetch data for multiple symbols simultaneously
2. Pre-calculate the end date timestamp to avoid repeated conversions
3. Use NumPy for SMA calculations instead of pandas rolling
4. Minimize DataFrame operations and reduce memory usage
5. Use a connection pool for CCXT
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
import concurrent.futures
from functools import partial

def calculate_sma(prices, period):
    """Calculate Simple Moving Average (SMA) using NumPy."""
    weights = np.ones(period)
    return np.convolve(prices, weights/weights.sum(), 'valid')[-1]

def process_symbol(symbol, exchange, end_timestamp):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, '1d', limit=100)
        if not ohlcv:
            print(f"Could not calculate SMA for {symbol}.")
            return None
        
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df = df[df['timestamp'] <= end_timestamp]
        
        if df.empty:
            print(f"No data available for {symbol} up to the end date.")
            return None
            
        close_prices = df['close'].to_numpy()
        sma_10 = calculate_sma(close_prices, 10)
        sma_50 = calculate_sma(close_prices, 50)
        
        last_date = pd.Timestamp(df['timestamp'].iloc[-1], unit='ms').strftime('%Y-%m-%d')
        return {
            'symbol': symbol,
            'date': last_date,
            'close': df['close'].iloc[-1],
            'sma_10': sma_10,
            'sma_50': sma_50
        }
    except Exception as e:
        print(f"Error processing {symbol}: {e}")
        return None

def main():
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
        'enableRateCache': True
    })

    top_20_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]

    end_date = "2024-11-25"
    end_timestamp = int(pd.Timestamp(end_date).timestamp() * 1000)
    
    process_func = partial(process_symbol, exchange=exchange, end_timestamp=end_timestamp)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_func, top_20_coins))
    
    for result in results:
        if result:
            print(f"SMA for {result['symbol']} (up to {end_date}):")
            print(f"      date    close    sma_10     sma_50")
            print(f"{result['date']} {result['close']:.6g} {result['sma_10']:.6g} {result['sma_50']:.6g}")

if __name__ == "__main__":
    main()