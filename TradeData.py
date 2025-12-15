import pandas as pd
import yfinance as yf
import mysql.connector
import ConfigTrade as Config


class TradeData:
    def __init__(self, ticker, start_date, end_date):
        yf.set_config(proxy=Config.proxy)
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.db = mysql.connector.connect(
            host="192.168.31.81",
            user="mysql",
            password="~Liujianzhe168",
            database="trade_data"
        )
        

    def fetch_data(self):
        """Fetch historical trade data from Yahoo Finance."""
        # self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date, interval='1d')
        df_list = []
        for ticker in self.ticker:
            data = yf.download(ticker, group_by="Ticker", period='2d')
            data['ticker'] = ticker  # Add ticker column
            df_list.append(data)
        data = pd.concat(df_list)
        return data

    def get_summary(self):
        """Get a summary of the fetched trade data."""
        if self.data is not None:
            return self.data.describe
        else:
            raise ValueError("Data not fetched yet. Call fetch_data() first.")

    def save_to_mysql(self, table_name):
        """Save the fetched data to a MySQL database."""
        if self.data is not None:
            self.data.to_sql(name=table_name, con=self.db, if_exists='replace', index=True)
        else:
            raise ValueError("Data not fetched yet. Call fetch_data() first.")


# Example usage:
if __name__ == "__main__":
    trade_data = TradeData(ticker=['AAPL', 'MSFT'], start_date="2022-06-01", end_date="2022-12-31")
    data = trade_data.fetch_data()
    data.to_csv('ticker.csv')
    # trade_data.save_to_mysql(table_name="tsla_trade_data")
    # print(trade_data.get_summary())