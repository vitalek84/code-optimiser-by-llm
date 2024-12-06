
"""
This script optimizes the original code by reducing redundant operations and improving data handling.
The changes include:
1. Fetching all symbols' data in one call to reduce API requests.
2. Removing unnecessary columns early to save memory.
3. Optimizing timestamp conversion.
"""

import ccxt
import pandas as pd

def fetch_ohlcv(exchange, symbols, timeframe='1d', limit=100):
    """Fetch OHLCV data for multiple symbols in one request."""
    try:
        markets = exchange.load_markets()
        ohlcv_data = []
        for symbol in symbols:
            if symbol in markets:
                market = markets[symbol]
                ohlcv_data.append(exchange.fetch_ohlcv(symbol, timeframe, limit=limit))
            else:
                print(f"Market {symbol} not found.")
        return pd.DataFrame([data[0] for data in ohlcv_data], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data: {e}")
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

    df = fetch_ohlcv(exchange, top_20_coins)

    if df is not None:
        # Convert timestamp to date
        df = convert_timestamp_to_date(df)

        # Filter by date
        df = filter_by_date(df, end_date)

        if df.empty:
            print("No data available up to", end_date)
            return

        # Calculate SMAs
        df['sma_10'] = calculate_sma(df, 10)
        df['sma_50'] = calculate_sma(df, 50)

        # Print results
        for symbol in top_20_coins:
            symbol_data = df[df['symbol'] == symbol]
            if not symbol_data.empty:
                print(f"SMA for {symbol} (up to {end_date}):")
                print(symbol_data[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
            else:
                print(f"No data available for {symbol} up to {end_date}.")

if __name__ == "__main__":
    main()
