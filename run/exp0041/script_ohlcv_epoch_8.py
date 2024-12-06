
"""
In the previous iteration, the execution time remained unchanged, which means no performance gains were achieved. I notice that
both base and previous iterations perform conversion and filtering as single steps independently for each symbol. Also, if there's no data for a certain date,
it skips calculation and moves to the next symbol immediately. Here are steps to improve performance:

1. Optimize Data Fetching: Parallelize the fetching of data across the top 20 coins using an asynchronous approach, which can significantly reduce waiting time for each HTTP request to complete.

2. Efficient Data Handling: Try combining all DataFrame transformations into a single step to minimize memory copying and improve operations speed.

3. Print Optimization: Adjust the printing of missing/invalid data messages to reduce I/O overhead.

By implementing these changes, the script should achieve better performance than the previous version by minimizing HTTP latency and excessive data manipulation.
"""

import ccxt.async_support as ccxt
import pandas as pd
import asyncio
from datetime import datetime


async def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    """Fetch OHLCV data for a given symbol asynchronously."""
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


def calculate_sma(df, period_10, period_50):
    """Calculate Simple Moving Averages for both 10 and 50-day periods."""
    df['sma_10'] = df['close'].rolling(window=period_10).mean()
    df['sma_50'] = df['close'].rolling(window=period_50).mean()
    return df


def process_dataframe(df, end_date):
    """Convert date, filter by date, and calculate SMAs in one step."""
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')
    df = df[pd.to_datetime(df['timestamp'], unit='ms') <= pd.Timestamp(end_date)].reset_index(drop=True)
    
    if not df.empty:
        df = calculate_sma(df, 10, 50)
    return df


async def main():
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    top_20_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]

    end_date = "2024-11-25"

    tasks = [fetch_ohlcv(exchange, symbol) for symbol in top_20_coins]
    dataframes = await asyncio.gather(*tasks)

    for symbol, df in zip(top_20_coins, dataframes):
        if df is not None:
            df = process_dataframe(df, end_date)
            last_entry = df.tail(1)
            if last_entry.empty:
                print(f"No data available or valid for {symbol} up to {end_date}.")
            else:
                print(f"SMA for {symbol} (up to {end_date}):")
                print(last_entry[['date', 'close', 'sma_10', 'sma_50']].to_string(index=False))
        else:
            print(f"Could not calculate SMA for {symbol}.")
    
    await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())
