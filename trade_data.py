"""Module providing a class for fetching and managing trade data."""

import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
import config


class TradeData:
    """Class for fetching and managing trade data from Yahoo Finance."""
    def __init__(self, start_date=None, end_date=None, ticker=None):
        yf.set_config(proxy=config.PROXY)
        # Avoid using a mutable default argument; copy the default ticker list if not provided
        if ticker is None:
            # make a shallow copy to avoid accidental external mutation
            self.ticker = list(config.TICKERS)
        else:
            # ensure ticker is a list
            if isinstance(ticker, (list, tuple, set)):
                self.ticker = list(ticker)
            else:
                self.ticker = [ticker]
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.db = create_engine(config.MYSQL_CONNECTION_STRING)

    def fetch_data(self):
        """
        Fetch trade data for the specified tickers and date range.
        and store it in the database.
        Returns:
            list of pd.DataFrame: List of dataframes containing trade data for each ticker."""
        dfs = [yf.download(
            ticker,
            group_by="Ticker",
            start=self.start_date,
            end=self.end_date, interval='1d')
            for ticker in self.ticker]
        for df, ticker in zip(dfs, self.ticker):
            df.columns =[s[1] for s in df.columns.tolist()]
            df.reset_index(inplace=True)
            df.to_sql(name=ticker, con=self.db, if_exists='replace', index=True)
        return dfs


# Example usage:
if __name__ == "__main__":
    trade_data = TradeData(
        ticker=config.TICKERS,
        start_date="1990-01-01",
        end_date=pd.Timestamp.today().strftime('%Y-%m-%d'))
    trade_data.fetch_data()
