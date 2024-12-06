
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


def convert_timestamp_to_date(df):
    """Convert UNIX timestamp to human-readable date."""
    pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df['date'] = df['timestamp'].dt.tz_convert('America/New_York').dt.strftime('%Y-%m-%d')
    return df



def main():
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    top_20_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]

    end_date = "2024-11-25"

    for symbol in top_20_coins:
        df = fetch_ohlcv(exchange, symbol)
        if not df.empty:
            df = convert_timestamp_to_date(df)
            df = df[pd.to_datetime(df['date']).dt.date <= pd.to_datetime(end_date)]

            if not df.empty:
                df = df.astype({'open': float, 'high': float, 'low': float, 'close': float, 'volume': float})
                df['sma_10'] = calculate_sma(df, 10)
                df['sma_50'] = calculate_sma(df, 50)


                print(f"SMA for {symbol} (up to {end_date}):")
                print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))

if __name__ == "__main__":
    main()
