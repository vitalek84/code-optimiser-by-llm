
"""
In the previous scripts the only 
"""
import ccxt
import pandas as pd
from datetime import datetime
import time


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

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

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

    # Execute faster
    for chunk in chunks(top_20_coins, 5):

        # Get multiple coins ohlcv simultaniously
        ohlcv_list = []
        for symbol in chunk:
            start_time = time.time()
            ohlcv = fetch_ohlcv(exchange, symbol)
            end_time = time.time()
            print(f"{symbol} fetched within: {(end_time - start_time) * 1000} ms")
            ohlcv_list.append(ohlcv)

        # Process ohlcv list 
        data = pd.DataFrame()
        for ohlcv in ohlcv_list:
            if ohlcv is not None:
                # Convert timestamp to date
                ohlcv = convert_timestamp_to_date(ohlcv)

                # Filter by date
                ohlcv = filter_by_date(ohlcv, end_date)

                if not ohlcv.empty:
                    # Calculate SMAs
                    ohlcv['sma_10'] = calculate_sma(ohlcv, 10)
                    ohlcv['sma_50'] = calculate_sma(ohlcv, 50)

                    # Append to result dataframe
                    data = pd.concat([data, ohlcv])

        # Print results
        # HINT FOR LLM: Should be printed in sequence like in list top_20_coins. Always!!!
        for symbol in chunk:
            result_chunk = data[data['symbol']==symbol]
            if not result_chunk.empty:
                print(f"SMA for {symbol} (up to {end_date}):")
                print(result_chunk[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
            else:
                print(f"No data available for {symbol} up to {end_date}.")

if __name__ == "__main__":
    main()
