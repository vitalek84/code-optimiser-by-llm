
"""
For the first optimization iteration, I'll focus on several key improvements:

1. Parallel Processing: Since we're fetching data for multiple coins independently, we can use concurrent.futures to parallelize the API calls.
2. Optimized DataFrame Operations:
   - Pre-allocate the timestamp conversion using pd.to_datetime once
   - Use vectorized operations instead of multiple conversions
3. Memory Efficiency:
   - Only keep necessary columns
   - Use more efficient data types
4. Reduced API Overhead:
   - Set custom timeout for API calls
   - Implement rate limiting more efficiently

Expected improvement: The parallel processing should significantly reduce the total execution time as API calls are the main bottleneck.
"""

import ccxt
import pandas as pd
from datetime import datetime
import concurrent.futures
from functools import partial

def fetch_ohlcv(exchange, symbol, end_date, timeframe='1d', limit=100):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        if not ohlcv:
            return None
        
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[df['timestamp'] <= pd.Timestamp(end_date)].reset_index(drop=True)
        
        if df.empty:
            return None
            
        df['date'] = df['timestamp'].dt.strftime('%Y-%m-%d')
        df['sma_10'] = df['close'].rolling(window=10).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        return df[['date', 'close', 'sma_10', 'sma_50']].tail(1)
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def process_symbol(symbol, exchange, end_date):
    df = fetch_ohlcv(exchange, symbol, end_date)
    if df is not None:
        print(f"SMA for {symbol} (up to {end_date}):")
        print(df.to_string(index=False))
    else:
        print(f"Could not calculate SMA for {symbol}.")

def main():
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
        'timeout': 30000,
    })

    top_20_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]

    end_date = "2024-11-25"
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        process_func = partial(process_symbol, exchange=exchange, end_date=end_date)
        executor.map(process_func, top_20_coins)

if __name__ == "__main__":
    main()
