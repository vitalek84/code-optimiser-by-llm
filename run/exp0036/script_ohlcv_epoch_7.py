"""
I noticed that the results of the reference version and my previous version are different. The main issues are:
1. SMA calculations show NaN values which means we don't have enough data for calculation
2. The order of output for DOT/USDT is different from reference
3. The limit parameter in fetch_ohlcv might be too small for SMA calculations

Optimization approach for this version:
1. Increase the limit parameter to ensure enough data for SMA calculations
2. Use pandas more efficiently by pre-allocating DataFrames
3. Reduce datetime conversions by doing them once
4. Maintain strict order of output
5. Use numpy for faster calculations
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime

def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_sma(prices, period):
    return pd.Series(prices).rolling(window=period, min_periods=period).mean()

def process_data(df, end_date):
    if df is None or df.empty:
        return None
    
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[df['datetime'] <= pd.Timestamp(end_date)].reset_index(drop=True)
    
    if not df.empty:
        df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
        df['sma_10'] = calculate_sma(df['close'].values, 10)
        df['sma_50'] = calculate_sma(df['close'].values, 50)
    
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
        df = fetch_ohlcv(exchange, symbol, limit=200)
        df = process_data(df, end_date)
        
        if df is not None and not df.empty:
            print(f"SMA for {symbol} (up to {end_date}):")
            print(df[['date', 'close', 'sma_10', 'sma_50']].tail(1).to_string(index=False))
        else:
            print(f"Could not calculate SMA for {symbol}.")

if __name__ == "__main__":
    main()