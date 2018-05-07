# -*-coding : utf-8 -*-

from strategy import *
import math


class CellRatio(Strategy):

    def __init__(self, code, basePrice, baseAmount, apRation):
        ''' apRatio delta a / delta p'''
        super().__init__(code)
        self.__basePrice = basePrice
        self.__baseAmount = baseAmount
        self.__apRation = apRation

    def judge(self):
        cpos = self.position()
        cp = self.getCurrentPrice()
        ratio = (float(cp) - self.__basePrice) / self.__basePrice * 100
        ratio = math.floor(ratio) if ratio > 0 else math.ceil(ratio)
        aRation = ratio * self.__apRation
        targetP100 = int(self.__baseAmount) / 100 - \
            math.floor(aRation * self.__baseAmount / 10000)
        amount = (int(cpos) / 100 - targetP100) * 100
        print(str(ratio), str(aRation), str(amount))
        print(str(amount), str(cp), str(cpos))
        return (int(amount), cpos, cp)


if __name__ == '__main__':
    c1 = CellRatio('512000', 0.85, 28600, 2)
    while True:
        c1.exeStrategy()
