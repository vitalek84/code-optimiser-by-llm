import ccxt
import pandas as pd
from datetime import datetime


def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    """Fetch OHLCV data for a given symbol."""
    df = pd.DataFrame(
        exchange.fetch_ohlcv(symbol, timeframe, limit=limit),
        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
    )
    return df


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

    all_results = {}
    for coin in top_20_coins:
        try:
            # Fetch data for coin
            df = fetch_ohlcv(exchange, coin)

            if df is not None:
                # Convert timestamp to date
                df = convert_timestamp_to_date(df)

                # Filter by date
                df = filter_by_date(df, end_date)

                if not df.empty:
                    # Calculate SMAs
                    df['sma_10'] = calculate_sma(df, 10)
                    df['sma_50'] = calculate_sma(df, 50)

                    all_results[coin] = df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_dict(orient="records")[0]
        except Exception:
            print(f"Error fetching data for {coin}.")

    # Print results
    for coin, data in all_results.items():
        # HINT FOR LLM: Should be printed in the list top_20_coins. Always!!!
        print(f"SMA for {coin} (up to {end_date}):")
        print(pd.DataFrame(all_results).to_string())


if __name__ == "__main__":
    main()
