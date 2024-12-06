"""
I will optimize the script with the following improvements:
1. Use concurrent.futures for parallel API calls to reduce total execution time
2. Reduce DataFrame operations by:
   - Pre-allocating DataFrame columns
   - Using vectorized operations where possible
   - Minimizing date conversions
3. Cache exchange instance to avoid recreation
4. Implement error handling for parallel execution
5. Ensure results are printed in the exact order as top_20_coins list
6. Store results in a dictionary first, then print in order to maintain sequence
"""

import ccxt
import pandas as pd
import concurrent.futures
from datetime import datetime

def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return df, symbol
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, symbol

def process_symbol_data(df_tuple, end_date):
    if df_tuple is None or df_tuple[0] is None:
        return None, df_tuple[1]
    
    df, symbol = df_tuple
    
    # Convert timestamp to datetime once
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
    
    # Filter by date
    mask = df['datetime'] <= pd.Timestamp(end_date)
    if not mask.any():
        return None, symbol
    
    df = df[mask].reset_index(drop=True)
    
    # Calculate SMAs using vectorized operations
    df['sma_10'] = df['close'].rolling(window=10).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    
    result = df[['date', 'close', 'sma_10', 'sma_50']].tail(1)
    return result, symbol

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
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_symbol = {executor.submit(fetch_ohlcv, exchange, symbol): symbol 
                          for symbol in top_20_coins}
        
        for future in concurrent.futures.as_completed(future_to_symbol):
            df_tuple = future.result()
            result, symbol = process_symbol_data(df_tuple, end_date)
            if result is not None:
                results[symbol] = result

    # Print results in order of top_20_coins
    for symbol in top_20_coins:
        if symbol in results:
            print(f"SMA for {symbol} (up to {end_date}):")
            print(results[symbol].to_string(index=False))
        else:
            print(f"Could not calculate SMA for {symbol}.")

if __name__ == "__main__":
    main()