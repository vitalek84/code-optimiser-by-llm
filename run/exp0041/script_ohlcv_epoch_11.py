
"""
In the previous iteration, the code execution time was still quite long and no improvements had yet been made.
To optimize execution time, I will take the following steps:

1. Use threading to fetch data for multiple symbols concurrently, which will help to take advantage of I/O-bound operations when communicating with the exchange.
2. Pre-compile frequent dataframe operations to achieve efficiency.
3. Evaluate if some of the computed values can be cached or re-used, although due to fresh trading data, it may or may not be applicable.
4. Ensure all date conversions happen as few times as possible.
5. Avoid the unnecessary conversion of timestamps into different formats multiple times.
"""

import ccxt
import pandas as pd
from datetime import datetime
import threading

def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    """Fetch OHLCV data for a given symbol."""
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_sma(df, period):
    """Calculate Simple Moving Average (SMA) for the close prices."""
    return df['close'].rolling(window=period).mean()

def preprocess_and_calculate(df, end_date, symbol):
    if df is not None:
        # Convert UNIX timestamp to datetime once
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        # Filter the OHLCV data up to the end_date
        df = df[df['datetime'] <= pd.Timestamp(end_date)].reset_index(drop=True)

        if df.empty:
            print(f"No data available for {symbol} up to {end_date}.")
            return

        # Calculate SMAs
        df['sma_10'] = calculate_sma(df, 10)
        df['sma_50'] = calculate_sma(df, 50)
        df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')

        # Print results
        print(f"SMA for {symbol} (up to {end_date}):")
        print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
    else:
        print(f"Could not calculate SMA for {symbol}.")

def main():
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    # Top 10 coins by market cap
    top_10_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]

    end_date = "2024-11-25"
    threads = []

    # Fetch data in separate threads to speed up I/O operations
    for symbol in top_10_coins:
        df = fetch_ohlcv(exchange, symbol)
        
        # Using threading to concurrently process data
        t = threading.Thread(target=preprocess_and_calculate, args=(df, end_date, symbol))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
