import yfinance as yf
import pandas as pd
import ConfigTrade as Config
from sqlalchemy import create_engine


yf.set_config(proxy=Config.proxy)
engine = create_engine('mysql+pymysql://mysql:~Liujianzhe168@192.168.31.81/trade_data')
# connection = sql.connect(
#     host="192.168.31.81",
#     user="mysql",
#     password="~Liujianzhe168",
#     database="trade_data"
# ) 

# print(connection.is_connected())

data = yf.download(['AAPL', 'MSFT'], group_by="ticker", start="2022-06-01", end="2022-12-31", interval='1d')
data.drop(data.index[[3]], axis=0, inplace=True)
print(data)
data.to_csv('ticker.csv')
data.to_sql(con=engine, name="trade_data", if_exists='replace', index=True)
data = pd.read_sql_query("SELECT * FROM trade_data;", con=engine)
data.to_csv('ticker_sql.csv')