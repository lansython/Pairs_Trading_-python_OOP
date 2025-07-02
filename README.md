# Python-lightgbm-trading-algorrithm

This repository contains a simple **statistical arbitrage** strategy using **pairs trading** based on cointegration analysis over a 3-year historical period. It identifies two co-moving stocks and generates long/short signals based on deviations from their mean-reverting spread.

---

## 📈 Strategy Overview

- **Concept**: Pairs trading exploits mean-reverting behavior between two cointegrated assets. When the spread diverges beyond a threshold, the strategy enters a position betting on convergence.
- **Selection**: Uses historical closing prices to identify the best pair of cointegrated stocks.
- **Execution**:
  - Long one stock and short the other when the spread deviates significantly from its mean.
  - Exit positions when the spread reverts.
- **Backtest Period**: ~3 years of historical daily data.

---

## 🧠 Key Components

| File | Description |
|------|-------------|
| `PairsTradingStrategy.py` | Implements the signal generation logic using cointegration and z-score thresholds |
| `portfolio.py` | Simulates position management, NAV tracking, and order generation |
|  notebook (main) | Runs the backtest loop across grouped dates and evaluates performance |
| `data/` | Folder containing historical price data (long-format CSV) |

---

## 📊 Performance Metrics (Example)

At the end of a backtest, the strategy reports:

- ✅ Final Net Asset Value (NAV)
- 📈 Annualized return
- 📉 Annualized volatility
- Annualized Sharp Ratio
- 🖼️ NAV time series plot
