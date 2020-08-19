#!/usr/bin/env python
# coding: utf-8

# In[10]:


from __future__ import (absolute_import, division, print_function, unicode_literals)

import backtrader as bt
import datetime
import os.path
import sys
import math
get_ipython().run_line_magic('matplotlib', 'inline')


# In[11]:


# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
        ('pfast', 50),
        ('pslow', 9),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        #adding sma indicator
        
        sma_fast = bt.indicators.SimpleMovingAverage(period=self.params.pfast)
        sma_slow = bt.indicators.SimpleMovingAverage(period=self.params.pslow)
        
        self.crossover = bt.indicators.CrossOver(sma_fast, sma_slow)
        
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' % (order.executed.price, 
                                                                               order.executed.value, 
                                                                               order.executed.comm))
                
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' % (order.executed.price, 
                                                                                order.executed.value, 
                                                                                order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
    
    
    
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))
    
    
    
    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.crossover < 0:
                # current price greater than the sma

                # BUY, BUY, BUY!!! (with default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            # Already in the market ... we might sell
            if self.crossover > 0:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
                
class LongOnly(bt.Sizer):
    params = (('stake', 1),)
    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            divide = math.floor(cash/data.open[0])
            self.p.stake = divide
            return self.p.stake
        
        # Sell situation
        position = self.broker.getposition(data)
        if not position.size:
            return 0  # do not sell if nothing is open
        return self.p.stake


# In[12]:


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    
    #add Strategy
    cerebro.addstrategy(TestStrategy)
    
    #datafeed
    data = bt.feeds.YahooFinanceData(dataname = 'RELIANCE.NS',
                                        fromdate = datetime.datetime(2019, 7, 31),
                                        todate = datetime.datetime(2020, 7, 31), reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)
    
    #initial cash
    cerebro.broker.setcash(200000.0)
    
    # stake size
    cerebro.addsizer(LongOnly)
    
    # Set the commission - in percent
    cerebro.broker.setcommission(commission=0.001)
    
    start_portfolio_value = cerebro.broker.getvalue()
    
    #stdstats parameter removes stats data while plotting
    cerebro.run(stdstats=True)

    end_portfolio_value = cerebro.broker.getvalue()
    
    pnl = end_portfolio_value - start_portfolio_value 
    print('Starting Portfolio Value: %.2f' % start_portfolio_value) 
    print('Final Portfolio Value: %.2f' % end_portfolio_value) 
    print('PnL: %.2f' % pnl)
    
    # Plot the result
    cerebro.plot()


# In[ ]:




