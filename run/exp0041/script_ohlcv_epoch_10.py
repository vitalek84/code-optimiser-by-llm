
"""
I noticed that the results of the reference version and my previous version are different. 
The results were printed in a different order than specified in the top_20_coins list. 
To address this issue, I will ensure the processing and printing of the results occur in the correct sequence.
Additionally, to optimize the execution time, I'm considering reducing the number of conversions and optimizing the SMA calculation by directly working on relevant slices of the data.
Let's attempt to apply these optimizations.
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


def calculate_sma(series, period):
    """Calculate Simple Moving Average (SMA) using a window sum to reduce operation overhead."""
    return series.rolling(window=period).mean()


def process_data(df, symbol, end_date):
    """Process the data for the given symbol."""
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[df['datetime'] <= pd.Timestamp(end_date)].copy()

    if df.empty:
        print(f"No data available for {symbol} up to {end_date}.")
        return None

    df['sma_10'] = calculate_sma(df['close'], 10)
    df['sma_50'] = calculate_sma(df['close'], 50)
    df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')

    return df[['date', 'close', 'sma_10', 'sma_50']].tail(1)


def main():
    # Initialize exchange (Binance in this example)
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    # Fetch the top 10 coins by market cap (manually selected for simplicity)
    top_20_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]

    # Restrict data till this date
    end_date = "2024-11-25"

    for symbol in top_20_coins:
        df = fetch_ohlcv(exchange, symbol)
        if df is not None:
            result = process_data(df, symbol, end_date)
            if result is not None:
                print(f"SMA for {symbol} (up to {end_date}):")
                print(result.to_string(index=False))

if __name__ == "__main__":
    main()
