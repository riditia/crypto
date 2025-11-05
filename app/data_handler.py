import pandas as pd
from datetime import datetime, timedelta
from app.api_client import CoinSwitchAPIClient

def get_historical_data(api_client: CoinSwitchAPIClient, symbol: str, interval: int, days_history: int = 30):
    """
    Fetches historical k-line data and returns it as a pandas DataFrame.

    :param api_client: An instance of CoinSwitchAPIClient.
    :param symbol: The trading symbol (e.g., 'BTC/INR').
    :param interval: The candle interval in minutes (e.g., 30).
    :param days_history: The number of days of historical data to fetch.
    :return: A pandas DataFrame with OHLCV data, or None if an error occurs.
    """
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(days=days_history)).timestamp() * 1000)

    raw_data = api_client.get_candles(symbol, interval, start_time, end_time)

    if not raw_data or 'result' not in raw_data:
        print("Failed to fetch historical data or 'result' key not found.")
        return None

    if not raw_data['result']:
        print("No historical data returned for the specified range.")
        return pd.DataFrame()

    df = pd.DataFrame(raw_data['result'])

    # Rename columns for clarity and consistency
    df.rename(columns={
        'o': 'open',
        'h': 'high',
        'l': 'low',
        'c': 'close',
        # The API response key for volume is 'volume'
        'start_time': 'timestamp'
    }, inplace=True)

    df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='ms')
    df.set_index('timestamp', inplace=True)

    # Convert OHLCV columns to numeric types
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col])

    return df
