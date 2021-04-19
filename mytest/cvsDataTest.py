#%%

import datetime
import os.path
import sys

import backtrader as bt

#Create a Stratey
class TestStrategy(bt.Strategy):
    # params = (
    #     ('exitbars',5),
    # )
    params = (
        ('maperiod',5),
        ('printlog', False),
    )

    def log(self,txt,dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod
        )

        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0],plot=False)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                # self.log('BUY EXECUTED, %.2f' % order.executed.price)
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                    order.executed.value,
                    order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            # elif order.issell():
            else:
                # self.log('SELL EXECUTED, %.2f' % order.executed.price)
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            # if self.dataclose[0] < self.dataclose[-1]:
            #     if self.dataclose[-1] < self.dataclose[-2]:
            #         self.log('BUY CREATE, %.2f' % self.dataclose[0])
            #         self.order = self.buy()
            if self.dataclose[0] > self.sma[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        else:
            # if len(self) >= (self.bar_executed+5):
            if self.dataclose[0] < self.sma[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # datapath = os.path.join(modpath,'../datas/orcl-1995-2014.txt')
    datapath = os.path.join(modpath, '../datas/btc-kline-sort.csv')

    # data = bt.feeds.YahooFinanceCSVData(
    #     dataname = datapath,
    #     fromdate = datetime.datetime(2000,1,1),
    #     todate = datetime.datetime(2000,12,31),
    #     reverse=False
    # )
    data = bt.feeds.GenericCSVData(
        dataname=datapath,
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1,
        # dtformat=('%Y-%m-%dT%H:%M:%S.%fZ'),
        dtformat=('%Y-%m-%d %H:%M:%S+00:00'),
        # dtformat=('%Y-%m-%d'),
        # tmformat=('%H:%M:%S'),
        fromdate = datetime.datetime(2021,3,1),
        todate = datetime.datetime(2021,3,30)
    )

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    # cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()

