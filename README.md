
# Backtesting Trading Strategies

This repo contains code for various tasks require for algo trading right from fetching the data, choosing initial capital to invest, commission for broker and various trading strategies for back testing. This repo is for learning purpose and will keep on adding more code as and when I learn.

The "multiple SMA" file makes use of the backtrader library in python and lets you backtrade any of the stock of your preference, from any start to stop date and it'll give you the overall valuations of your portfolio at the stop date after using different sma crossovers in a range for example 10-30.

For now this uses Simple Moving Average (SMA) trading strategy for backtesting. Later, I'll add other trading strategies for other stocks.

### Prerequisites

* Python 3.7 & above
* Basic trading knowledge (Technical indicators)

### Running the tests

Currently, the backtesting can be done for following two tasks

- Check the reliability of a trading strategy (_SMA crossover for now_) by checking the portfolio value after certain back testing period
- Use multiple period SMA over a stock and tell which one worked best by calculating the final portfolio value against each of them
- Generate charts & check the buy/sell options over the ![plot](images/Reliance.png)


### File description

1. multiple_sma.py : use multiple SMA over a stock and tell which SMA worked best by calculating the final portfolio value against each SMA


### Built with

- [Backtrader](https://pypi.org/project/backtrader/) - Python Library used
- Find the docs for backtrader [here](https://www.backtrader.com/docu/)
