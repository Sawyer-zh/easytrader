# encoding=utf8

import easytrader
import time
import tushare as ts

user = easytrader.use('dfcf')

user.prepare('./dfcf.json')

yes = ts.get_k_data('512000', start='2018-01-01')
yesColse = yes['close'].values[-1]

buy = 0
sell = 0

while True:
    # ratio = float(currentPrice) / float(yesColse)
    data = user.position
    for i in data['Data']:
        print(i)
    today = ts.get_realtime_quotes('131810')
    currentPrice = today['price'][0]
    print(currentPrice)
    # print(currentPrice)
    # print(yesColse)
    # print(ratio)
    # if ratio >= 1.05:
    #     if sell < 3 :
    #         user.sell('512000',str(currentPrice),'1000')
    #         sell += 1
    #         print("sell %s" % sell)
    # if ratio <=0.99:
    #     if buy < 3:
    #         user.buy('512000',str(currentPrice),'100')
    #         buy+= 1
    #         print("buy %s" % buy)
    time.sleep(60)
