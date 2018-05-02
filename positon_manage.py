import easytrader
import tushare as ts
import math
import time

user = easytrader.use('dfcf')
user.prepare('./dfcf.json')


def get_position(code):
    pJson = user.position
    for item in pJson['Data']:
        if item['Zqdm'] == code:
            return item['Zqsl']
    else:
        return False


def get_current_price(code):
    today = ts.get_realtime_quotes(code)
    return today['price'][0]


def do_dsz(code, total):
    currentPrice = float(get_current_price(code))
    position = int(get_position(code))
    diff = currentPrice * position - total
    amount = math.floor(diff / currentPrice / 100)
    print('cp ->' + str(currentPrice))
    print('p->' + str(position))
    print('diff->' + str(diff))
    print('a->' + str(amount))
    if amount > 0:
        user.sell(code, str(currentPrice), amount * 100)
        print('sell')
        time.sleep(120)
    elif amount < -1:
        user.buy(code, str(currentPrice), (-1 - amount) * 100)
        print('buy')
        time.sleep(120)
    else:
        time.sleep(1)


if __name__ == '__main__':
    while True:
        do_dsz('512000', 24300)
