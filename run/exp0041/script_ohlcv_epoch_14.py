
"""
I noticed that the previous and initial versions had the same execution times and matched results, indicating correctness. However, to optimize performance and reduce execution time, I will make the following changes:
1. Utilize multithreading to parallelize the data fetching and processing for multiple symbols concurrently.
2. Suppress output messages to minimize I/O operations, which can be time-consuming.
3. Ensure that the changes maintain the integrity of the output to match the reference results.
"""

import ccxt
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    """Fetch OHLCV data for a given symbol."""
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        return None


def calculate_sma(df, period):
    """Calculate Simple Moving Average (SMA) for the close prices."""
    return df['close'].rolling(window=period).mean()


def convert_timestamp_to_date(df):
    """Convert UNIX timestamp to human-readable date."""
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')
    return df


def filter_by_date(df, end_date):
    """Filter the OHLCV data to include rows up to the specified end_date."""
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df[df['datetime'] <= pd.Timestamp(end_date)].reset_index(drop=True)


def process_symbol(exchange, symbol, end_date):
    """Process each symbol: fetch data, filter by date, calculate SMA, and return results."""
    df = fetch_ohlcv(exchange, symbol)
    if df is not None:
        df = convert_timestamp_to_date(df)
        df = filter_by_date(df, end_date)
        if not df.empty:
            df['sma_10'] = calculate_sma(df, 10)
            df['sma_50'] = calculate_sma(df, 50)
            return (f"SMA for {symbol} (up to {end_date}):",
                    df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
    return (f"Could not calculate SMA for {symbol}.", None)


def main():
    # Initialize exchange (Binance in this example)
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    # Fetch the top 10 coins by market cap (manually selected for simplicity)
    top_10_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]

    # Restrict data till this date
    end_date = "2024-11-25"

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(
            lambda symbol: process_symbol(exchange, symbol, end_date),
            top_10_coins
        ))

    for result in results:
        if result[1] is not None:
            print(result[0])
            print(result[1])
        else:
            print(result[0])


if __name__ == "__main__":
    main()
