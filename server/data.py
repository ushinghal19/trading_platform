import pandas as pd
from api.alphavantage import get_alphavantage_data
from api.finnhub import get_finnhub_data
from utils import calculate_historical_trading_signals, calculate_new_trading_signals


class Data:
    """ Object that represents current state of data """

    def __init__(self):
        self.dataframe = pd.DataFrame()

    def update_historical_data(self, ticker: str, interval: str) -> None:
        # Get new data for the ticker
        df = get_alphavantage_data(ticker, interval)
        new_data = calculate_historical_trading_signals(df, interval)

        # If the main DataFrame is empty, initialize it with new_data
        if self.dataframe.empty:
            self.dataframe = new_data
        else:
            # Concatenate the new data to the existing DataFrame
            self.dataframe = pd.concat([self.dataframe, new_data])

        # Sort the dataframe by the index, which is 'datetime'
        self.dataframe.sort_index(inplace=True)
        return

    def update_current_quote(self, ticker: str, interval: str) -> None:
        # Get new data for the ticker from Finnhub
        new_data_df = get_finnhub_data(ticker)

        # Check if new data's timestamp is after the last timestamp
        if not self.dataframe.empty and new_data_df.index[0] > self.dataframe.index[-1]:
            # Concatenate new data to the existing DataFrame
            self.dataframe = pd.concat([self.dataframe, new_data_df])

            # Calculate and update trading signals for the newly added row
            calculate_new_trading_signals(self.dataframe, ticker, interval)
        else:
            print("New data is not more recent than the existing data. No update performed.")
        return

    def remove_ticker_data(self, ticker: str) -> None:
        # Delete's all rows in self.dataframe where ticker == ticker
        self.dataframe = self.dataframe[self.dataframe.ticker != ticker]
        return


    def get_data_for_datetime(self, datetime_str):
        # Convert the input string to a pandas datetime object
        datetime = pd.to_datetime(datetime_str)

        nearest_timestamp = self.dataframe.index[0]
        # Find the nearest datetime to the provided datetime
        # I tried using get_loc and as_of methods but they didn't work
        for timestamp in self.dataframe.index:
            if timestamp <= datetime:
                nearest_timestamp = timestamp
            else:
                break
        # Filter rows that match the nearest datetime
        matching_rows = self.dataframe[self.dataframe.index == nearest_timestamp]
        # Reset index to remove timestamp index
        matching_rows.reset_index(drop=True, inplace=True)
        # Return the specific columns for those rows
        return matching_rows[['ticker', 'price', 'signal']]

    def get_dataframe(self):
        """ Used for CSV Generation. """
        return self.dataframe

#
# data = Data()
# data.update_historical_data('AAPL', '60min')
# data.update_historical_data('MSFT', interval='60min')
# # data.update_current_quote('AAPL', '60min')
# # data.update_current_quote('MSFT', '60min')
# # data.dataframe.to_csv('data.csv')
# data.get_data_for_datetime('2024-03-08T14:00:00')
# # # print(data.dataframe)
