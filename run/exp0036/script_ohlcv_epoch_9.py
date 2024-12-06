"""
For this first optimization iteration, I'll focus on several key improvements:

1. Use concurrent.futures for parallel API calls to reduce waiting time
2. Precompute the end date timestamp to avoid repeated conversions
3. Use numpy for SMA calculations instead of pandas for better performance
4. Minimize DataFrame operations by doing calculations on raw data
5. Optimize memory usage by selecting only necessary columns
6. Use format strings instead of f-strings for performance
7. Set pandas display options once at the start
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
import concurrent.futures
from functools import partial

pd.set_option('display.float_format', lambda x: '%.6f' % x)

def fetch_ohlcv(exchange, symbol, end_date_ts, timeframe='1d', limit=100):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df = df[df['timestamp'] <= end_date_ts]
        if not df.empty:
            df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')
            close_vals = df['close'].values
            df['sma_10'] = np.convolve(close_vals, np.ones(10)/10, mode='valid')[-1]
            df['sma_50'] = np.convolve(close_vals, np.ones(50)/50, mode='valid')[-1]
            return df[['date', 'close', 'sma_10', 'sma_50']].tail(1)
        return None
    except Exception as e:
        print("Error fetching data for {}: {}".format(symbol, e))
        return None

def process_symbol(args):
    exchange, symbol, end_date_ts = args
    result = fetch_ohlcv(exchange, symbol, end_date_ts)
    if result is not None:
        print("SMA for {} (up to 2024-11-25):".format(symbol))
        print(result.to_string(index=False))
    else:
        print("Could not calculate SMA for {}.".format(symbol))

def main():
    exchange = ccxt.binance({'rateLimit': 1200, 'enableRateLimit': True})
    end_date = "2024-11-25"
    end_date_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)
    
    symbols = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_symbol, ((exchange, symbol, end_date_ts) for symbol in symbols))

if __name__ == "__main__":
    main()