
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

    # Lists to store SMA and pandas DataFrames for each coin
    sma_10_list = []
    sma_50_list = []
    df_list = []

    for symbol in top_20_coins:

        # Fetch OHLCV data
        df = fetch_ohlcv(exchange, symbol)

        # Convert timestamp to date, filter data, and calculate SMAs if data is not None
        if df is not None:
            df = convert_timestamp_to_date(df)
            df = filter_by_date(df, end_date)
            if not df.empty:
                sma_10_list.append(calculate_sma(df, 10).iloc[-1])
                sma_50_list.append(calculate_sma(df, 50).iloc[-1])
                df_list.append(df)

    # Create a DataFrame to store coin info, SMAs
    df_results = pd.DataFrame({
        'Coin': top_20_coins,
        'SMA_10': sma_10_list,
        'SMA_50': sma_50_list
    })

    # Restrict data till this date
    df_results = filter_by_date(df_results, end_date)

    # Print results
    print("SMA results for multiple coins up to {end_date}:\n")
    print(df_results[['Coin', 'close', 'SMA_10', 'SMA_50']].to_string(index=False))


if __name__ == "__main__":
    main()
