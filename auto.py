# encoding=utf8

import easytrader
import time
import tushare as ts

user = easytrader.use('dfcf')

user.prepare('./dfcf.json')

yes = ts.get_k_data('159916',start='2018-01-01')
yesColse = yes['close'].values[-1]
print(yes)
print(yesColse)

buy = 0
sell =  0

while True:
    today = ts.get_realtime_quotes('159916')
    currentPrice = today['price']
    if currentPrice / yesColse >= 1.1:
        if sell <= 10 :
            user.sell('159916',str(currentPrice),'100')
            sell += 1
    if currentPrice / yesColse <= 0.9:
        if buy <= 10:
            user.buy('159916',str(currentPrice),'100')
            buy+= 1
    time.sleep(30)