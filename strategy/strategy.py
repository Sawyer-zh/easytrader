# -*-coding:utf-8-*-
import sys
sys.path.insert(0, '..')
import easytrader
import time
import tushare as ts

user = easytrader.use('dfcf')
user.prepare('./../dfcf.json')


class Strategy (object):
    """ strategy for trade"""

    def __init__(self, code):
        self.__code = code

    def exeStrategy(self):
        (amount, position, price) = self.judge()
        if amount == 0:
            print('do nothing')
        else:
            wtbh = self.trade(amount, price)
            self.check(wtbh, position)
        time.sleep(10)

    def judge(self):
        '''need to implement by subclass'''
        pass

    def trade(self, amount, price):
        if amount > 0:
            print('sell :' + str(int(amount)) + "  ---  " + str(price))
            return user.sell(self.__code, price, int(amount))
        elif amount < 0:
            print('buy :' + str(0 - int(amount)) + "  ---  " + str(price))
            return user.buy(self.__code, price, int(0 - amount))

    def check(self, wtbh, positon, interval=5):
        ''' check if succeed'''
        for _ in range(5):
            time.sleep(interval)
            currentPositon = self.position()
            if currentPositon and currentPositon != str(positon):
                return True
        user.cancelOrder(wtbh)
        print("order cancel")

    def position(self):
        pJson = user.position
        for item in pJson['Data']:
            if item['Zqdm'] == self.__code:
                return item['Zqsl']
        else:
            return False

    def getCurrentPrice(self):
        today = ts.get_realtime_quotes(self.__code)
        return today['price'][0]
