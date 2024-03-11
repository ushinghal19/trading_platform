import pandas as pd


def calculate_historical_trading_signals(df: pd.DataFrame, interval: str) -> pd.DataFrame:
    """ Using the momentum trading strategy to calculate signals. """

    interval_minutes = int(interval[:-3])
    window_size = ((60//interval_minutes) * 24)
    # Calculate rolling mean and standard deviation.
    df['S_avg'] = df['price'].rolling(window=window_size).mean()
    df['Sigma'] = df['price'].rolling(window=window_size).std()
    # Generate signals
    df.loc[df['price'] > df['S_avg'] + df['Sigma'], 'signal'] = 1  # Buy
    df.loc[df['price'] < df['S_avg'] - df['Sigma'], 'signal'] = -1  # Sell
    # Create a column that shows how many positions are open at each time
    df['position'] = df['signal'].cumsum()
    # Calculate the pnl
    df['pnl'] = df['position'].shift(1) * (df['price'] - df['price'].shift(1))
    df['cum_pnl'] = df['pnl'].cumsum()

    return df


def calculate_new_trading_signals(df: pd.DataFrame, ticker: str, interval: str) -> pd.DataFrame:
    """Update trading signals and PnL for the last row in the DataFrame."""
    interval_minutes = int(interval[:-3])
    window_size = ((60 // interval_minutes) * 24)

    # Get only the part of the dataframe corresponding to the ticker
    ticker_df = df[df['ticker'] == ticker]
    # Calculate S_avg and Sigma for the last row
    df.at[df.index[-1], 'S_avg'] = ticker_df['price'][-window_size:].mean()
    df.at[df.index[-1], 'Sigma'] = ticker_df['price'][-window_size:].std()
    # Update signal for the last row
    last_price = ticker_df.iloc[-1]['price']
    last_s_avg = ticker_df.iloc[-1]['S_avg']
    last_sigma = ticker_df.iloc[-1]['Sigma']
    if last_price > last_s_avg + last_sigma:
        df.at[ticker_df.index[-1], 'signal'] = 1  # Buy
    elif last_price < last_s_avg - last_sigma:
        df.at[ticker_df.index[-1], 'signal'] = -1  # Sell
    else:
        df.at[ticker_df.index[-1], 'signal'] = 0  # Hold/no action

    # Update position for the last row by adding to the previous position depending on the signal
    df.at[ticker_df.index[-1], 'position'] = ticker_df.iloc[-2]['position'] + ticker_df.iloc[-1]['signal']
    # Calculate PnL for the last row

    price_diff = ticker_df.iloc[-1]['price'] - ticker_df.iloc[-2]['price']
    df.at[ticker_df.index[-1], 'pnl'] = ticker_df.iloc[-2]['signal'] * price_diff
    # Update cumulative PnL for the last row
    df.at[ticker_df.index[-1], 'cum_pnl'] = ticker_df.iloc[-2]['cum_pnl'] + ticker_df.iloc[-1]['pnl']

    return df
