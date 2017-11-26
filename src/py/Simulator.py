import tushare as ts
import config
import talib
import matplotlib.pyplot as plt
import tc_macd
import pandas as pd
import datetime
import Position
import utils

import logging

logger = logging.getLogger(__name__)


class Simulator:

    def __init__(self, name, pool, start=None, end=None):
        self.name = name
        self.instrument_pool = pool
        self.positions = {}
        self.cash = 1000000
        self.income = 1
        self.data = pd.DataFrame()
        self.date = ""

        if start:
            self.start = start
        else:
            self.start = config.default_start_date

        if end:
            self.end = end
        else:
            self.end = datetime.datetime.now().strftime(config.date_pat)

        # print self.instrument_pool.keys
        self.data[config.date_key] = self.instrument_pool[self.instrument_pool.keys()[0]][config.date_key]
        self.data[config.income_key] = 0.0


    def buy(self, instrument):
        if instrument not in self.positions.keys():
            # data frame of inst
            df = self.instrument_pool[instrument]
            self.positions[instrument] = Position.Position(instrument)
            price = self.positions[instrument].cost = df.loc[df.loc[df[config.date_key]==self.date].index][config.close_key].values[0]

            can_buy = int(self.cash / price)
            self.positions[instrument].quantity = can_buy

            self.cash -= price * can_buy

            logger.info("%s: Buy: %s X %s at cost: %s" % (self.name, instrument, can_buy, price))

    def sell(self, instrument):
        if instrument in self.positions.keys():
            deleted = self.positions.pop(instrument)

            df = self.instrument_pool[instrument]
            cost = deleted.cost
            price = df.loc[df.loc[df[config.date_key]==self.date].index][config.close_key].values[0]
            self.cash += price * deleted.quantity
            # self.income = ((price - cost) / cost + 1) * self.income

            logger.info("%s: Sell: %s X %s at price: %s" % (self.name, instrument, deleted.quantity, price))

    def update(self):
        logger.warning("EOD: %s" % self.date)
        logger.warning("cash: %s" % self.cash)
        total = self.cash

        for instrument in self.positions.keys():
            df = self.instrument_pool[instrument]
            qtt = self.positions[instrument].quantity
            price = df.loc[df.loc[df[config.date_key]==self.date].index][config.close_key].values[0]
            # print("#################")
            logger.warning("position: %s" % instrument)
            logger.warning("quantity: %s" % qtt)
            logger.warning("current price: %s" % price)
            # print("#################")

            value_amt = qtt * price
            total += value_amt

        logger.warning("Account value: %s" % total)
        income = (total - config.bash_cash) / config.bash_cash
        logger.warning("Account income: %s" % income)

        self.data.loc[utils.get_df_index_by_col_value(self.data, config.date_key, self.date), config.income_key] = income