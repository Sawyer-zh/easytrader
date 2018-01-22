# encoding=utf8

import dfcf_trader


autoTrader = dfcf_trader.DFCFTrader()

autoTrader.prepare('../dfcf.json')

print(autoTrader.balance)