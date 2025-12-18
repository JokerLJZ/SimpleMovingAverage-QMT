import yfinance as yf
import pandas as pd
import config as Config
from sqlalchemy import create_engine


yf.set_config(proxy=Config.proxy)
engine = create_engine('mysql+pymysql://mysql:~Liujianzhe168@192.168.31.81/trade_data')
ticker = ['510300.SS']
data = yf.download(tickers=ticker, start="2022-12-01", end="2022-12-31", interval='1d')
data["Ticker"] = ticker[0]
data.columns =[str(s[0]) for s in data.columns.tolist()]
data.reset_index(inplace=True)
data = data.head()

# print(data.columns.tolist(), data.index.tolist())

# data["Date"] = data.index.date

# data.index = pd.to_datetime(data.index).date


data.to_csv('ticker.csv')
data.to_sql(con=engine, name="trade_data", if_exists='replace', index=False)
data = pd.read_sql_query("SELECT * FROM trade_data;", con=engine)
print(data)
data.to_csv('ticker_sql.csv')