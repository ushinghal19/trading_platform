import pandas as pd
from server.data import Data
from unittest import mock


""" Note, these tests worked when I moved them into the data file and ran them, however due to import issues
    they don't fully work here. I tried forver to fix the issue but then decided to move onto Part 2 of the project. """
""" With more time, I would've written more comprehensive tests for each function I wrote in this assignment."""

def test_update_historical_data():
    """ Test the update_historical_data method of the Data class."""

    data = Data()
    data.update_historical_data('AAPL', '60min')
    assert not data.dataframe.empty
    assert data.dataframe.columns.tolist() == ['price', 'ticker', 'S_avg', 'Sigma', 'signal', 'position', 'pnl', 'cum_pnl']
    assert all(data.dataframe.ticker == 'AAPL')

    data.update_historical_data('MSFT', interval='60min')
    assert not data.dataframe.empty
    assert all(data.dataframe.ticker.isin(['AAPL', 'MSFT']))

def test_update_current_quote():
    """ Test the update_current_quote method of the Data class."""
    info = {
        'price': [100],
        'ticker': ['AAPL'],
        'S_avg': [0],
        'Sigma': [0],
        'signal': [0],
        'position': [0],
        'pnl': [0],
        'cum_pnl': [0]
    }

    index = pd.to_datetime(['2024-03-10 04:00:00'])
    df = pd.DataFrame(info, index=index)
    with mock.patch('server.api.finnhub.get_finnhub_data') as mock_finnhub:
        mock_finnhub.return_value = df
        data = Data()
        length = len(data.dataframe)
        data.update_historical_data('AAPL', '60min')
        data.update_current_quote('AAPL', '60min')
        new_length = len(data.dataframe)
        assert new_length == length + 1


def test_update_old_quote():
    """ Test the update_current_quote method of the Data class with old data."""

    info = {
        'price': [100],
        'ticker': ['AAPL'],
        'S_avg': [0],
        'Sigma': [0],
        'signal': [0],
        'position': [0],
        'pnl': [0],
        'cum_pnl': [0]
    }

    index = pd.to_datetime(['2020-02-16 04:00:00'])
    df = pd.DataFrame(info, index=index)
    with mock.patch('server.api.finnhub.get_finnhub_data', return_value=df):
        data = Data()
        data.update_historical_data('AAPL', '60min')
        length = len(data.dataframe)
        data.update_current_quote('AAPL', '60min')
        new_length = len(data.dataframe)
        assert new_length == length
