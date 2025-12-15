# SimpleMovingAverage-QMT

通过 MiniQMT 实现基于 MA(简单移动平均) 的实盘与回测示例。

## 主要内容
- 实盘接入：使用 [Trade.py](Trade.py)，通过 MiniQMT 连接并登录账户（配置见 [`qmt_path`](ConfigTrade.py) 与 [`account`](ConfigTrade.py)）。
  - 关键符号：[`xttrader.XtQuantTrader`](Trade.py)、[`xt_trader`](Trade.py)
- 回测示例：使用 [BackTrader.py](BackTrader.py) 提供的简单均线交叉策略（SMA crossover）。
  - 关键符号：[`SMAStrategy`](BackTrader.py)、[`load_csv_to_feed`](BackTrader.py)、[`make_synthetic_feed`](BackTrader.py)、[`run`](BackTrader.py)

## 快速开始

1. 安装依赖（示例）：
```sh
pip install backtrader pandas numpy xtquant
```

2. 配置实盘参数：
- 编辑 [ConfigTrade.py](ConfigTrade.py) 中的 [`qmt_path`](ConfigTrade.py) 和 [`account`](ConfigTrade.py)。

3. 运行回测：
- 使用内置合成数据：
```sh
python BackTrader.py
```
- 使用 CSV 数据：
```sh
python BackTrader.py --csv path/to/data.csv --cash 10000 --fast 10 --slow 30 --plot
```
BackTrader 的入口函数为 [`run`](BackTrader.py)。

4. 运行实盘（请在确认配置和风控后执行）：
```sh
python Trade.py
```
Trade 脚本使用 [`xttrader.XtQuantTrader`](Trade.py) 连接 MiniQMT 并通过 [`qmt_path`](ConfigTrade.py) 和 [`account`](ConfigTrade.py) 登录。

## 文件索引
- [BackTrader.py](BackTrader.py) — 回测策略与工具（包含 [`SMAStrategy`](BackTrader.py)）
- [Trade.py](Trade.py) — MiniQMT 实盘接入示例（使用 [`xttrader.XtQuantTrader`](Trade.py)）
- [ConfigTrade.py](ConfigTrade.py) — 配置文件，包含 [`qmt_path`](ConfigTrade.py) 和 [`account`](ConfigTrade.py)
- [.gitignore](.gitignore)

## 注意事项
- 实盘前请在安全的环境中充分测试并确认风控规则。
- 根据实际 MiniQMT/经纪商要求调整下单与资金管理逻辑。

## 许可证
请在仓库中添加适当的 LICENSE 文件以声明许可信息。
