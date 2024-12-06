
"""
This version of the script aims to optimize execution time by reducing the number of API calls and parallelizing data fetching using asynchronous programming with asyncio. Additionally, it uses vectorized operations for date conversion and filtering, which are generally faster than loop-based operations.
"""

import ccxt.async_support as ccxt  # Asynchronous ccxt
import pandas as pd
from datetime import datetime
import asyncio

async def fetch_ohlcv_async(exchange, symbol, timeframe='1d', limit=100):
    """Asynchronously fetch OHLCV data for a given symbol."""
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_sma(df, period):
    """Calculate Simple Moving Average (SMA) for the close prices."""
    return df['close'].rolling(window=period).mean()

def convert_timestamp_to_date(df):
    """Convert UNIX timestamp to human-readable date using vectorized operations."""
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')
    return df

def filter_by_date(df, end_date):
    """Filter the OHLCV data to include rows up to the specified end_date using vectorized operations."""
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df[df['datetime'] <= pd.Timestamp(end_date)].reset_index(drop=True)

async def main():
    # Initialize exchange (Binance in this example)
    exchange = await ccxt.binance({
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

    tasks = []
    for symbol in top_20_coins:
        tasks.append(fetch_ohlcv_async(exchange, symbol))

    dfs = await asyncio.gather(*tasks)

    for df, symbol in zip(dfs, top_20_coins):
        if df is not None:
            # Convert timestamp to date
            df = convert_timestamp_to_date(df)

            # Filter by date
            df = filter_by_date(df, end_date)

            if df.empty:
                print(f"No data available for {symbol} up to {end_date}.")
                continue

            # Calculate SMAs
            df['sma_10'] = calculate_sma(df, 10)
            df['sma_50'] = calculate_sma(df, 50)

            # Print results
            print(f"SMA for {symbol} (up to {end_date}):")
            print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
        else:
            print(f"Could not calculate SMA for {symbol}.")

if __name__ == "__main__":
    asyncio.run(main())
