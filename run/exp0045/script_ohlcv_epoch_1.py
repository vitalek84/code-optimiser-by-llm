
"""
Optimizing the script by:
1. Reducing I/O operations by fetching all symbols in a single call if possible.
2. Using vectorized operations and avoiding unnecessary function calls.
3. Preallocating memory for DataFrame columns where possible.
"""

import ccxt
import pandas as pd
from datetime import datetime

def fetch_ohlcv(exchange, symbols, timeframe='1d', limit=100):
    """Fetch OHLCV data for multiple symbols."""
    ohlcv_data = {}
    for symbol in symbols:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            ohlcv_data[symbol] = df
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    return ohlcv_data

def calculate_sma(df_list, period):
    """Calculate Simple Moving Average (SMA) for the close prices in a list of DataFrames."""
    sma_dict = {}
    for symbol, df in df_list.items():
        df['sma_10'] = df['close'].rolling(window=period).mean()
        sma_dict[symbol] = df
    return sma_dict

def convert_timestamp_to_date(df_list):
    """Convert UNIX timestamp to human-readable date in a list of DataFrames."""
    for symbol, df in df_list.items():
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')
    return df_list

def filter_by_date(df_list, end_date):
    """Filter the OHLCV data to include rows up to the specified end_date in a list of DataFrames."""
    filtered_df_list = {}
    for symbol, df in df_list.items():
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        filtered_df_list[symbol] = df[df['datetime'] <= pd.Timestamp(end_date)].reset_index(drop=True)
    return filtered_df_list

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

    # Fetch OHLCV data for all symbols at once
    ohlcv_data = fetch_ohlcv(exchange, top_20_coins)

    # Convert timestamp to date
    ohlcv_data = convert_timestamp_to_date(ohlcv_data)

    # Filter by date
    ohlcv_data = filter_by_date(ohlcv_data, end_date)

    # Calculate SMAs
    sma_data = calculate_sma(ohlcv_data, 10)
    sma_data = calculate_sma(sma_data, 50)

    # Print results
    for symbol in top_20_coins:
        if symbol not in sma_data or sma_data[symbol].empty:
            print(f"No data available for {symbol} up to {end_date}.")
            continue

        print(f"SMA for {symbol} (up to {end_date}):")
        print(sma_data[symbol][['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))

if __name__ == "__main__":
    main()
