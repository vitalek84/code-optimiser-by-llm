import concurrent.futures
import ccxt
import pandas as pd
from datetime import datetime

symbol_data_lock = None


def fetch_ohlcv_wrapped(exchange, symbol, timeframe='1d', limit=100):
    global symbol_data_lock
    if symbol_data_lock is None:
        symbol_data_lock = [threading.Lock() for _ in range(5)]

    with symbol_data_lock[int(symbol[0])]:
        return fetch_ohlcv(exchange, symbol, timeframe, limit)


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

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_ohlcv_wrapped, exchange, symbol) for symbol in top_20_coins]

        dfs = [future.result() for future in futures]

    # I noticed that the previous version successfully finds all the data for every symbol but takes lots of time because
    # functions are running one by one in order. So the idea is for this iteration is to run every function concurrently.
    # As a metric here we measure the total execution time for all the instruments and want to reduce it.
    # To run functions concurrently we can create a thread pool, add all the functions to run and wait until results are
    # acquired. In the provided code I’m creating thread pool of 5 threads. And since we have top_20_coins it means we run
    # 5 functions at the same time and then when the first 5 are executed we move to 6, 7, 8, 9, and 10 function. My asusmption in
    # this case is that total execution time will be reduced at least in half. For example, if the total time was about 12 seconds
    # than it should now take about 12 / 5 = 2.4 seconds.

    for df in dfs:
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
            # HINT FOR LLM: Should be printed in sequence like in list top_20_coins. Always!!!
            print(f"SMA for {symbol} (up to {end_date}):")
            print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
        else:
            print(f"Could not calculate SMA for {symbol}.")


if __name__ == "__main__":
    main()
