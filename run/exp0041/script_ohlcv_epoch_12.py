
"""
Chain of Thought:
1. The initial and the previous iterations are exactly the same, with no optimization and similar execution time.
2. Since both previous iterations are similar, the task remains to optimize data fetching and processing speed.
3. Repeated conversion of timestamps in multiple places may introduce unnecessary overhead.
4. `pandas` operations are known to be optimized, but reducing data size early helps in efficient processing.
5. Check if updating the `pandas` version offers performance improvements in timestamp conversion and rolling calculations.
6. Using list comprehension instead of loops where possible also tends to enhance performance.
7. To avoid multiple conversions and repetitive operations, streamline processes and minimize data transformations.
8. Check if utilizing `NumPy` for numerical operations can provide some speedup over `pandas`.
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime

def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    """Fetch OHLCV data for a given symbol and return as DataFrame."""
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_sma(close_prices, period):
    """Calculate Simple Moving Average (SMA) for the close prices."""
    return pd.Series(close_prices).rolling(window=period).mean().values

def process_dataframe(df, end_date):
    """Process the data frame: filter by date, convert timestamps."""
    df = df[df['timestamp'] <= pd.Timestamp(end_date).timestamp() * 1000]
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')
    return df

def main():
    # Initialize exchange (Binance in this example)
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    # Fetch the top 20 coins by market cap (manually selected for simplicity)
    top_20_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]

    # Restrict data till this date
    end_date = "2024-11-25"

    for symbol in top_20_coins:
        df = fetch_ohlcv(exchange, symbol)

        if df is not None and not df.empty:
            df = process_dataframe(df, end_date)

            if df.empty:
                print(f"No data available for {symbol} up to {end_date}.")
                continue

            # Calculate SMAs using numpy for potential speed gains
            sma_10 = calculate_sma(df['close'].to_numpy(), 10)
            sma_50 = calculate_sma(df['close'].to_numpy(), 50)

            # Add columns to the DataFrame
            df['sma_10'] = sma_10
            df['sma_50'] = sma_50

            # Print results
            print(f"SMA for {symbol} (up to {end_date}):")
            print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
        else:
            print(f"Could not calculate SMA for {symbol}.")

if __name__ == "__main__":
    main()
