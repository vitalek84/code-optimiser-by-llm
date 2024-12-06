
"""
Optimization Plan:
1. I will remove redundant conversions and calculations where possible, specifically the conversion of timestamps twice.
2. I'll consider using the NUMBA library to compile certain operations for faster array computations.
3. Grouping actions may reduce repetitive DataFrame operations.
4. I noticed no previous iteration errors; thus, the base and previous versions shared the same execution time.
5. I will focus on reducing DataFrame operations and enhancing loop operations.
"""

import ccxt
import pandas as pd
from datetime import datetime
from numba import jit

@jit(nopython=True)
def calculate_sma_jit(values, period):
    """Numba optimized function to calculate SMAs."""
    result = [float('nan')] * len(values)
    for i in range(period - 1, len(values)):
        result[i] = sum(values[i - period + 1:i + 1]) / period
    return result

def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    """Fetch OHLCV data for a given symbol."""
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def preprocess_dataframe(df, end_date):
    """Preprocess dataframe: convert timestamp and filter by date."""
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[df['timestamp'] <= pd.Timestamp(end_date)]
    return df.reset_index(drop=True)

def main():
    # Initialize exchange (Binance in this example)
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    # Fetch the top 10 coins by market cap
    top_10_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]

    # Restrict data till this date
    end_date = "2024-11-25"

    for symbol in top_10_coins:

        df = fetch_ohlcv(exchange, symbol)

        if df is not None:
            # Preprocess dataframe
            df = preprocess_dataframe(df, end_date)

            if df.empty:
                print(f"No data available for {symbol} up to {end_date}.")
                continue

            # Calculate SMAs using Numba optimized function
            df['sma_10'] = calculate_sma_jit(df['close'].values, 10)
            df['sma_50'] = calculate_sma_jit(df['close'].values, 50)

            # Assign date for readability
            df['date'] = df['timestamp'].dt.strftime('%Y-%m-%d')

            # Print results
            print(f"SMA for {symbol} (up to {end_date}):")
            print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
        else:
            print(f"Could not calculate SMA for {symbol}.")

if __name__ == "__main__":
    main()
