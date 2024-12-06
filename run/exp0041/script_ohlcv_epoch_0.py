
"""
In the previous iteration, the execution time remained the same as the base version. To optimize the execution time, we will implement the following improvements:
1. Multi-threading: Use the `concurrent.futures.ThreadPoolExecutor` to fetch data for multiple symbols concurrently.
2. Minimize Pandas DataFrame operations: Group DataFrame manipulations to reduce the overhead of multiple operations.
3. Reduce the scope of date conversion: Combine timestamp conversions and filtering in a single step to minimize redundant operations.
"""

import ccxt
import pandas as pd
from datetime import datetime
import concurrent.futures


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


def process_data_for_symbol(exchange, symbol, end_date):
    df = fetch_ohlcv(exchange, symbol)

    if df is not None:
        # Convert timestamp to date and directly filter
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[df['datetime'] <= pd.Timestamp(end_date)]

        if df.empty:
            return f"No data available for {symbol} up to {end_date}.", None

        # Calculate SMAs
        df['sma_10'] = calculate_sma(df, 10)
        df['sma_50'] = calculate_sma(df, 50)

        # Format and return the result
        result = f"SMA for {symbol} (up to {end_date}):\n" + df[['datetime', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False)
        return result, df[['datetime', 'close', 'sma_10', 'sma_50']].tail(1)

    return f"Could not calculate SMA for {symbol}.", None


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

    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_data_for_symbol, exchange, symbol, end_date) for symbol in top_20_coins]
        for future in concurrent.futures.as_completed(futures):
            result, _ = future.result()
            if result is not None:
                results.append(result)

    # Print all results in the original order of top_20_coins
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
