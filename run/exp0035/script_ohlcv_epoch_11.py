import ccxt
import pandas as pd
from datetime import datetime


def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    """Fetch OHLCV data for a given symbol."""
    data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    timestamp, open, high, low, close, volume = zip(*data)
    csv_arr = pd.DataFrame(
        list(zip(timestamp, open, high, low, close, volume)),
        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
    )
    
    return csv_arr



def calculate_sma(df, period):
    """Calculate Simple Moving Average (SMA) for the close prices."""
    return df['close'].rolling(window=period).mean()

def format_result(df, symbol: str, end_date: str):
    return f"SMA for {symbol} (up to {end_date}):\n" + df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False)



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
    results = []
    for symbol in top_20_coins:
        # print(f"\nFetching data for {symbol}...")
        df = fetch_ohlcv(exchange, symbol)
        if df.empty:
                print(f"No data available for {symbol} up to {end_date}.")
                continue

        # Calculate SMAs
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')
        df['timestamp'] = df['date']
        df = filter_by_date(df, end_date)
        
        df['sma_10'] = calculate_sma(df, 10)
        df['sma_50'] = calculate_sma(df, 50)
        results.append(format_result(df, symbol, end_date))
    
    # Print results
    print('\n'.join(results))


if __name__ == "__main__":
    main()
