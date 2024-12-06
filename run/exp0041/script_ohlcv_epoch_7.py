
"""
Chain of Thought:
1. I noticed that the previous script had a lot of redundant pandas conversions and filtering which might be slowing down the execution.
2. Instead of converting and filtering the DataFrame multiple times for each symbol, I will try to combine and streamline these transformations.
3. Limit the output of SMA calculation to the required date, reducing unnecessary calculations.
4. Use default data structures and functionalities instead of converting DataFrame when it's unnecessary.
5. Reduce any repeated operations within the loop.
6. Keep an eye on any potential parallel execution or bulk processing.
"""

import ccxt
import pandas as pd
from datetime import datetime

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

def process_ohlcv_data(df, end_date):
    """Convert and filter OHLCV data for processing."""
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[df['datetime'] <= pd.Timestamp(end_date)]
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

    # Restrict data until this date
    end_date = "2024-11-25"

    for symbol in top_20_coins:
        df = fetch_ohlcv(exchange, symbol)
        if df is not None and not df.empty:
            # Process data: convert timestamp and filter by date in one step
            df = process_ohlcv_data(df, end_date)

            if df.empty:
                print(f"No data available for {symbol} up to {end_date}.")
                continue

            # Calculate SMAs on filtered data
            df['sma_10'] = calculate_sma(df, 10)
            df['sma_50'] = calculate_sma(df, 50)

            # Tailor the result to the required final date only
            # Ensures we calculate and print for final date only
            df_final = df[df['date'] == end_date]

            if not df_final.empty:
                print(f"SMA for {symbol} (up to {end_date}):")
                print(df_final[['date', 'close', 'sma_10', 'sma_50']].to_string(index=False))
            else:
                print(f"Data exists but no valid entries for final date {end_date} for {symbol}.")
        else:
            print(f"Could not calculate SMA for {symbol}.")

if __name__ == "__main__":
    main()
