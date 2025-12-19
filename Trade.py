"""
Docstring for Trade
"""
import random
from xtquant import xttrader
from xtquant.xttype import StockAccount
import config

qmt_path = config.QMT_PATH
account = config.ACCOUNT

session_id = int(random.randint(100000, 999999))

xt_trader = xttrader.XtQuantTrader(qmt_path, session_id)
xt_trader.start()

connect_result = xt_trader.connect()

if connect_result == 0:
    print("Success to connect to QMT")
else:
    print("Fail to connect to QMT")
    exit()

acc = StockAccount(account)


subscribe_result = xt_trader.subscribe(acc)
if subscribe_result == 0:
    print("Success to login account")
else:
    print("Fail to login account")
    exit()

asset = xt_trader.query_stock_asset(acc)
print("Account Asset:", format(asset.cash))
