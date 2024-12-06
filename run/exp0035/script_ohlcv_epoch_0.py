
import ccxt
import pandas as pd
from datetime import datetime

def convert_timestamp_to_date(df):
    df['date'] = (pd.to_datetime(df['timestamp'], unit='ms')).dt.strftime('%Y-%m-%d')

def convert_timestamp_to_datetime(df):
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def main():

    # Exchange for fetching data
    exchange = ccxt.binance({'rateLimit': 1200, 'enableRateLimit': True})

    # Fetch popular coins and calculate SMAs for these over 10 and 50 days
    coins = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'XRP/USDT', 'DOGE/USDT', 'ADA/USDT', 'SOL/USDT', 'DOT/USDT', 'MATIC/USDT', 'SHIB/USDT']
    end_date = '2024-11-25'

    # Main loop for fetch data and calculate SMA for each coin
    for symbol in coins:
        # Fetch, convert timestamp to date and filter data
        df = exchange.fetch_ohlcv(symbol, '1d')
        df = convert_timestamp_to_date(df)
        df = df[df['date'] <= end_date].reset_index(drop=True)

        # Calculate SMAs for periods 10 and 50
        df['sma_10'] = df['close'].rolling(10).mean()
        df['sma_50'] = df['close'].rolling(50).mean()

        # Print results
        print(f"SMA for {symbol} (up to {end_date}): ")
        print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))

if __name__ == '__main__':
    main()

