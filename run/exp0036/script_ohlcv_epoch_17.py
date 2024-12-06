"""
I'll optimize the code with the following improvements:
1. Implement concurrent API calls using asyncio and aiohttp to fetch data in parallel
2. Use numpy for faster calculations of SMA instead of pandas
3. Minimize DataFrame operations and conversions
4. Maintain the exact order of results as in top_20_coins
5. Fix the results order issue from the previous version
"""

import ccxt.async_support as ccxt
import pandas as pd
import numpy as np
import asyncio
from datetime import datetime
from collections import OrderedDict

async def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return symbol, pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return symbol, None
    
def calculate_sma(close_prices, period):
    return np.convolve(close_prices, np.ones(period)/period, mode='valid')

async def process_symbol(exchange, symbol, end_date):
    symbol_data = await fetch_ohlcv(exchange, symbol)
    if symbol_data[1] is not None:
        df = symbol_data[1]
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df[df['datetime'] <= pd.Timestamp(end_date)].reset_index(drop=True)
        
        if not df.empty:
            close_prices = df['close'].values
            df['sma_10'] = np.nan
            df['sma_50'] = np.nan
            if len(close_prices) >= 50:
                sma_10 = calculate_sma(close_prices, 10)
                sma_50 = calculate_sma(close_prices, 50)
                df.loc[9:, 'sma_10'] = sma_10
                df.loc[49:, 'sma_50'] = sma_50
            
            df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
            result = df[['date', 'close', 'sma_10', 'sma_50']].tail(1)
            return symbol, result
    return symbol, None

async def main():
    exchange = ccxt.binance({
        'enableRateLimit': True,
        'rateLimit': 1200,
    })
    
    top_20_coins = [
        "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
        "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
    ]
    
    end_date = "2024-11-25"
    
    tasks = [process_symbol(exchange, symbol, end_date) for symbol in top_20_coins]
    results = await asyncio.gather(*tasks)
    await exchange.close()
    
    results_dict = OrderedDict((symbol, result) for symbol, result in results)
    
    for symbol in top_20_coins:
        if results_dict[symbol] is not None:
            print(f"SMA for {symbol} (up to {end_date}):")
            print(results_dict[symbol].to_string(index=False))
        else:
            print(f"Could not calculate SMA for {symbol}.")

if __name__ == "__main__":
    asyncio.run(main())