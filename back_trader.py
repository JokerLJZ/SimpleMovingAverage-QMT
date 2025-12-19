"""
Docstring for back_trader
"""

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class BackTrader:
    def __init__(self, initial_capital=10000, short_window=20, long_window=50):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.short_window = short_window
        self.long_window = long_window
        self.trades = []
        self.positions = []
        
    def generate_signals(self, df):
        """Generate SMA crossover signals"""
        df['SMA_short'] = df['close'].rolling(window=self.short_window).mean()
        df['SMA_long'] = df['close'].rolling(window=self.long_window).mean()
        df['signal'] = 0
        df.loc[df['SMA_short'] > df['SMA_long'], 'signal'] = 1
        df.loc[df['SMA_short'] <= df['SMA_long'], 'signal'] = 0
        df['position'] = df['signal'].diff()
        return df
    
    def backtest(self, df):
        """Run backtest on price data"""
        df = self.generate_signals(df)
        shares = 0
        
        for idx, row in df.iterrows():
            # Buy signal
            if row['position'] == 1:
                shares = self.capital / row['close']
                self.trades.append({'date': idx, 'type': 'BUY', 'price': row['close'], 'shares': shares})
            # Sell signal
            elif row['position'] == -1 and shares > 0:
                self.capital = shares * row['close']
                self.trades.append({'date': idx, 'type': 'SELL', 'price': row['close'], 'shares': shares})
                shares = 0
            
            self.positions.append({'date': idx, 'capital': self.capital, 'price': row['close']})
        
        return df
    
    def plot_results(self, df):
        """Plot trading results"""
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Plot price and SMAs
        ax.plot(df.index, df['close'], label='Price', linewidth=2)
        ax.plot(df.index, df['SMA_short'], label=f'SMA {self.short_window}', alpha=0.7)
        ax.plot(df.index, df['SMA_long'], label=f'SMA {self.long_window}', alpha=0.7)
        
        # Plot buy/sell signals
        buy_signals = df[df['position'] == 1]
        sell_signals = df[df['position'] == -1]
        ax.scatter(buy_signals.index, buy_signals['close'], color='green', marker='^', s=100, label='BUY')
        ax.scatter(sell_signals.index, sell_signals['close'], color='red', marker='v', s=100, label='SELL')
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.set_title('Simple Moving Average Backtest')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Generate sample data
    dates = pd.date_range('2023-01-01', periods=200, freq='D')
    prices = 100 + np.cumsum(np.random.randn(200) * 2)
    df = pd.DataFrame({'close': prices}, index=dates)
    
    # Run backtest
    trader = BackTrader(initial_capital=10000, short_window=20, long_window=50)
    df = trader.backtest(df)
    trader.plot_results(df)
    
    print(f"Trades executed: {len(trader.trades)}")
    print(f"Final capital: ${trader.capital:.2f}")