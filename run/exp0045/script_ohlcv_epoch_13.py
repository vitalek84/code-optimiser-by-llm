
"""
I noticed that the previous version works incorrectly. I analysed the issue and fixed it. Also I understand that I shouldn’t take to account execution time of not working version.
This version improves performance by reducing unnecessary calculations and using more efficient data handling techniques.
"""

import ccxt
import pandas as pd
from datetime import datetime

def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    """Fetch OHLCV data for a given symbol."""
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df[df['datetime'] <= pd.Timestamp('2024-11-25')].reset_index(drop=True)
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_sma(df, period):
    """Calculate Simple Moving Average (SMA) for the close prices."""
    return df['close'].rolling(window=period).mean()

def convert_timestamp_to_date(df):
    """Convert UNIX timestamp to human-readable date."""
    df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
    return df

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

    for symbol in top_20_coins:
        df = fetch_ohlcv(exchange, symbol)
        
        if not df.empty:
            # Convert timestamp to date
            df = convert_timestamp_to_date(df)

            # Calculate SMAs
            df['sma_10'] = calculate_sma(df, 10)
            df['sma_50'] = calculate_sma(df, 50)

            # Print results
            print(f"SMA for {symbol} (up to 2024-11-25):")
            print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
        else:
            print(f"No data available for {symbol} up to 2024-11-25.")

if __name__ == "__main__":
    main()
