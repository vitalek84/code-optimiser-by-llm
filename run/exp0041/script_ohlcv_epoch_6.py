
"""
I noticed that the results of the reference version and my previous version are different, I analysed the issue and tried to fix it. The errors indicate that the fetch_ohlcv method is returning None, suggesting a mismatch in the column count when forming the DataFrame. To address this, I'll ensure that the dataframe is formed correctly using ohlcv data. Additionally, I will improve the execution time by optimizing the dataframe operations and reducing any redundant computations.
"""

import ccxt
import pandas as pd


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
    return df['close'].rolling(window=period, min_periods=1).mean()


def filter_and_process_data(df, end_date):
    """Convert UNIX timestamp to date, filter and process data."""
    if df is None or df.empty:
        return None

    # Filter and convert data
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[df['datetime'] <= pd.Timestamp(end_date)].copy()

    if df.empty:
        return None

    df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
    df['sma_10'] = calculate_sma(df, 10)
    df['sma_50'] = calculate_sma(df, 50)

    return df[['date', 'close', 'sma_10', 'sma_50']]


def main():
    # Initialize exchange (Binance in this example)
    exchange = ccxt.binance({'rateLimit': 1200, 'enableRateLimit': True})

    # Fetch the top 20 coins by market cap (manually selected for simplicity)
    top_20_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]

    # Restrict data till this date
    end_date = "2024-11-25"

    for symbol in top_20_coins:
        df = fetch_ohlcv(exchange, symbol)

        processed_df = filter_and_process_data(df, end_date)
        if processed_df is not None and not processed_df.empty:
            print(f"SMA for {symbol} (up to {end_date}):")
            print(processed_df.tail(1).to_string(index=False))
        else:
            print(f"Could not calculate SMA for {symbol}.")


if __name__ == "__main__":
    main()
