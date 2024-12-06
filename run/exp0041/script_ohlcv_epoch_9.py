
"""
I noticed that the execution time of the previous version is the same as the base version, indicating no improvement. I will attempt an optimization by making use of multi-threading to fetch OHLCV data concurrently for each symbol. This approach should potentially reduce the total execution time since fetching data over the network is often a bottleneck.
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
        print(f"Error fetching data for {symbol}: {e}")
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
    """Process each symbol to fetch data, filter and calculate SMAs."""
    df = fetch_ohlcv(exchange, symbol)
    if df is not None:
        df = convert_timestamp_to_date(df)
        df = filter_by_date(df, end_date)
        if df.empty:
            print(f"No data available for {symbol} up to {end_date}.")
            return
        df['sma_10'] = calculate_sma(df, 10)
        df['sma_50'] = calculate_sma(df, 50)
        print(f"SMA for {symbol} (up to {end_date}):")
        print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
    else:
        print(f"Could not calculate SMA for {symbol}.")

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

    with ThreadPoolExecutor(max_workers=5) as executor:
        for symbol in top_20_coins:
            executor.submit(process_symbol, exchange, symbol, end_date)

if __name__ == "__main__":
    main()
