from server.api.config import FINNHUB_API_KEY, FINNHUB_BASE_URL
import requests
import pandas as pd
from datetime import datetime

def process_finnhub_response(response_json: dict, symbol: str) -> pd.DataFrame:
    """ Process the data returned from Finnhub. """
    # Convert timestamp to datetime and create a DataFrame
    timestamp = datetime.fromtimestamp(response_json['t'])
    df = pd.DataFrame({
        'datetime': [timestamp],
        'price': [response_json['c']],
        'ticker': [symbol],
        'S_avg': [0],
        'Sigma': [0],
        'signal': [0],
        'position': [0],
        'pnl': [0],
        'cum_pnl': [0]
    })

    # Set 'datetime' as the index
    df.set_index('datetime', inplace=True)

    return df


def get_finnhub_data(symbol: str) -> pd.DataFrame:
    """ Get data from finnhub for a given symbol. """
    params = {
        'symbol': symbol,
        'token': FINNHUB_API_KEY
    }
    response = requests.get(f"{FINNHUB_BASE_URL}/quote", params=params)
    response_json = response.json()
    df = process_finnhub_response(response_json, symbol)
    return df
