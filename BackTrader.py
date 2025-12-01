import argparse
from datetime import datetime
import numpy as np
import pandas as pd
import backtrader as bt

#!/usr/bin/env python3
"""
BackTrader.py

Simple Moving Average crossover strategy using Backtrader.
Usage:
    python BackTrader.py --csv path/to/data.csv --cash 10000 --fast 10 --slow 30 --plot
If no CSV is provided a synthetic price series will be generated.
"""



class SMAStrategy(bt.Strategy):
    params = dict(period_fast=10, period_slow=30, stake=1)

    def __init__(self):
        self.sma_fast = bt.ind.SMA(self.data.close, period=self.p.period_fast)
        self.sma_slow = bt.ind.SMA(self.data.close, period=self.p.period_slow)
        self.crossover = bt.ind.CrossOver(self.sma_fast, self.sma_slow)

    def next(self):
        # Buy when fast SMA crosses above slow SMA, sell when it crosses below.
        if not self.position:
            if self.crossover > 0:
                self.buy(size=self.p.stake)
        else:
            if self.crossover < 0:
                self.close()


def load_csv_to_feed(path, fromdate=None, todate=None):
    """
    Load CSV into a Backtrader feed. Tries to handle common CSV formats.
    Expected columns: Date (or index), Open, High, Low, Close, Volume (optional)
    """
    df = pd.read_csv(path, parse_dates=True, index_col=0)
    # Normalize column names
    cols = {c.lower(): c for c in df.columns}
    mapping = {}
    for std in ("open", "high", "low", "close", "volume", "openinterest"):
        if std in cols:
            mapping[cols[std]] = std.capitalize() if std != "openinterest" else "OpenInterest"
    df = df.rename(columns=mapping)
    # Ensure required columns exist
    if "Close" not in df.columns:
        raise ValueError("CSV must contain a Close column")
    df = df.sort_index()
    # Slice date range if requested
    if fromdate:
        df = df[df.index >= fromdate]
    if todate:
        df = df[df.index <= todate]
    feed = bt.feeds.PandasData(dataname=df)
    return feed


def make_synthetic_feed(n=500, start_price=100.0, volatility=0.02):
    rng = np.random.default_rng(42)
    returns = rng.normal(loc=0.0002, scale=volatility, size=n)
    price = start_price * np.exp(np.cumsum(returns))
    dates = pd.date_range(end=datetime.today(), periods=n, freq="B")
    df = pd.DataFrame(index=dates)
    df["Close"] = price
    df["Open"] = df["Close"].shift(1).fillna(df["Close"])
    df["High"] = np.maximum(df["Open"], df["Close"]) * (1 + 0.001 * rng.random(n))
    df["Low"] = np.minimum(df["Open"], df["Close"]) * (1 - 0.001 * rng.random(n))
    df["Volume"] = (1e6 * (0.5 + rng.random(n))).astype(int)
    return bt.feeds.PandasData(dataname=df)


def run(args):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(args.cash)

    # Data feed
    if args.csv:
        feed = load_csv_to_feed(args.csv, fromdate=args.fromdate, todate=args.todate)
    else:
        feed = make_synthetic_feed()
    cerebro.adddata(feed)

    cerebro.addstrategy(SMAStrategy, period_fast=args.fast, period_slow=args.slow, stake=args.stake)

    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe", timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")

    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    results = cerebro.run()
    strat = results[0]

    print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")

    # Print analyzers
    if "sharpe" in strat.analyzers:
        try:
            sr = strat.analyzers.sharpe.get_analysis()
            print("Sharpe Ratio:", sr.get("sharperatio"))
        except Exception:
            pass

    if "drawdown" in strat.analyzers:
        dd = strat.analyzers.drawdown.get_analysis()
        print("Max Drawdown: {:.2f}%".format(dd.get("max", {}).get("drawdown", dd.get("maxdrawdown", 0))))

    if "trades" in strat.analyzers:
        ta = strat.analyzers.trades.get_analysis()
        print("Total Trades:", sum(ta.get(k, 0) for k in ["total", "closed", "won", "lost"]) if isinstance(ta, dict) else ta)

    if args.plot:
        cerebro.plot(style="candlestick")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Simple SMA crossover Backtrader example")
    p.add_argument("--csv", help="Path to CSV file with OHLC data", default=None)
    p.add_argument("--cash", type=float, default=10000.0, help="Starting cash")
    p.add_argument("--fast", type=int, default=10, help="Fast SMA period")
    p.add_argument("--slow", type=int, default=30, help="Slow SMA period")
    p.add_argument("--stake", type=int, default=1, help="Order size (shares)")
    p.add_argument("--plot", action="store_true", help="Show plot at the end")
    p.add_argument("--fromdate", type=lambda s: datetime.fromisoformat(s), default=None, help="ISO from date (YYYY-MM-DD)")
    p.add_argument("--todate", type=lambda s: datetime.fromisoformat(s), default=None, help="ISO to date (YYYY-MM-DD)")
    args = p.parse_args()
    run(args)