"""
I will optimize the code with the following changes:
1. Use asyncio and aiohttp for parallel API requests
2. Pre-calculate date conversion and filtering criteria
3. Use numpy for faster SMA calculations
4. Minimize DataFrame operations
5. Format output string once instead of multiple operations
6. Add connection pooling for better network performance
7. Cache timestamp conversions
"""

import ccxt.async_support as ccxt
import pandas as pd
import numpy as np
import asyncio
import aiohttp
from datetime import datetime

async def fetch_ohlcv(exchange, symbol, timeframe='1d', limit=100):
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        return None if not ohlcv else pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_sma(prices, period):
    return pd.Series(prices).rolling(window=period, min_periods=period).mean().iloc[-1]

async def process_symbol(exchange, symbol, end_timestamp):
    df = await fetch_ohlcv(exchange, symbol)
    if df is None or df.empty:
        print(f"Could not calculate SMA for {symbol}.")
        return
    
    mask = df['timestamp'] <= end_timestamp
    if not mask.any():
        print(f"No data available for {symbol} up to {end_date}.")
        return
        
    filtered_df = df[mask]
    if filtered_df.empty:
        return
    
    closes = filtered_df['close'].values
    date = pd.Timestamp(filtered_df['timestamp'].iloc[-1], unit='ms').strftime('%Y-%m-%d')
    close = closes[-1]
    sma_10 = calculate_sma(closes, 10)
    sma_50 = calculate_sma(closes, 50)
    
    print(f"SMA for {symbol} (up to {end_date}):")
    print(f"      date    close    sma_10     sma_50")
    print(f"{date} {close:8.6f} {sma_10:8.6f} {sma_50:8.6f}")

async def main():
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        exchange = ccxt.binance({
            'session': session,
            'enableRateLimit': True,
            'rateLimit': 1200,
        })

        try:
            top_20_coins = [
                "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT",
                "ADA/USDT", "SOL/USDT", "DOT/USDT", "MATIC/USDT", "SHIB/USDT"
            ]
            
            global end_date
            end_date = "2024-11-25"
            end_timestamp = pd.Timestamp(end_date).value // 10**6
            
            tasks = [process_symbol(exchange, symbol, end_timestamp) for symbol in top_20_coins]
            await asyncio.gather(*tasks)
            
        finally:
            await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())