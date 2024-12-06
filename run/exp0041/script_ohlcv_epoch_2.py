
"""
I noticed that the results of the reference version and my previous version are different, I analysed the issue and tried to fix it. So results should be the same in the current version.
- Introduced asynchronous requests for fetching data to allow concurrent fetching, which should reduce the total execution time significantly.
- Used numpy for SMA calculations instead of pandas rolling, which can be faster for simple calculations.
- Ensure the final print statements follow the same sequence as `top_20_coins` list.
- Made sure that the order of outputs is consistent with the original script.
"""

import ccxt
import pandas as pd
import numpy as np
import asyncio
from datetime import datetime


async def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    """Async Fetch OHLCV data for a given symbol."""
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


def calculate_sma_numpy(df, period):
    """Calculate Simple Moving Average (SMA) using numpy for the close prices."""
    return np.convolve(df['close'], np.ones(period), 'valid') / period


def convert_timestamp_to_date(df):
    """Convert UNIX timestamp to human-readable date."""
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')
    return df


def filter_by_date(df, end_date):
    """Filter the OHLCV data to include rows up to the specified end_date."""
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df[df['datetime'] <= pd.Timestamp(end_date)].reset_index(drop=True)


async def main():
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

    tasks = [fetch_ohlcv(exchange, symbol) for symbol in top_20_coins]
    dataframes = await asyncio.gather(*tasks)

    for symbol, df in zip(top_20_coins, dataframes):
        if df is not None:
            # Convert timestamp to date
            df = convert_timestamp_to_date(df)

            # Filter by date
            df = filter_by_date(df, end_date)

            if df.empty:
                print(f"No data available for {symbol} up to {end_date}.")
                continue

            # Calculate SMAs with numpy
            sma_10 = calculate_sma_numpy(df, 10)
            sma_50 = calculate_sma_numpy(df, 50)

            # Apply padding
            df['sma_10'] = np.pad(sma_10, (len(df) - len(sma_10), 0), mode='constant', constant_values=np.nan)
            df['sma_50'] = np.pad(sma_50, (len(df) - len(sma_50), 0), mode='constant', constant_values=np.nan)

            # Print results
            print(f"SMA for {symbol} (up to {end_date}):")
            print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
        else:
            print(f"Could not calculate SMA for {symbol}.")


if __name__ == "__main__":
    asyncio.run(main())
