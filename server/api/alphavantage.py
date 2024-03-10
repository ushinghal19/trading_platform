from server.api.config import *
import requests
from ratelimit import limits, sleep_and_retry
import pandas as pd


def process_alphavantage_response(response_json: dict, ticker: str) -> pd.DataFrame:
    """ Process the data returned from Alphavantage. """

    # Find the time series data
    time_series_key = next(k for k in response_json.keys() if 'Time Series' in k)
    time_series_data = response_json[time_series_key]

    # Transform the time series data into a pandas DataFrame
    df = pd.DataFrame.from_dict(time_series_data, orient='index')
    # Convert index to datetime and sort by date
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    # Convert all column names to lower case and all values to numeric type
    df.columns = [col.lower().split()[-1] for col in df.columns]
    df = df.apply(pd.to_numeric)

    # Select only the 'close' column and rename it to 'price'
    df = df[['close']].rename(columns={'close': 'price'})

    # Add additional required columns initialized to 0
    df['ticker'] = ticker
    df['S_avg'] = 0
    df['Sigma'] = 0
    df['signal'] = 0
    df['position'] = 0
    df['pnl'] = 0
    df['cum_pnl'] = 0

    return df


@sleep_and_retry
@limits(calls=ALPHAVANTAGE_CALLS, period=ALPHVANTAGE_SECONDS)
def get_alphavantage_data(symbol: str, interval: str) -> pd.DataFrame:
    """ Get data from alphavantage for a given symbol and interval. """
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'apikey': ALPHA_VANTAGE_API_KEY,
        'outputsize': 'full'
    }
    response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
    response_json = response.json()
    df = process_alphavantage_response(response_json, symbol)
    return df
