
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

    fastest_time =float('inf')  # Use this variable to save the best execution time.
    
    
    for coin in top_20_coins:
        df = fetch_ohlcv(exchange, coin)
        
        if df is not None:
            # Convert timestamp to date
            df = convert_timestamp_to_date(df)

            # Filter by date
            df = filter_by_date(df, end_date)

            if df.empty:
                print(f"No data available for {coin} up to {end_date}.")
                continue

            # Calculate SMAs
            df['sma_10'] = calculate_sma(df, 10)
            df['sma_50'] = calculate_sma(df, 50)
            
            
            current_duration = df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False)
            print(f"SMA for {coin} (up to {end_date}):\n{current_duration}")
            execution_time = 11766213  # PlaceHolder  In reality, execution time must be measured
            if execution_time < fastest_time:
                fastest_time = execution_time
                print(fastest_time)
                best_performing_code = current_duration
        else:
            print(f"Could not calculate SMA for {coin}.")


if __name__ == "__main__":
    main()
