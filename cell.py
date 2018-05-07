# -*- coding:utf-8 -*-

import pymysql
import tushare as ts
import time
import easytrader
from threading import Thread

user = easytrader.use('dfcf')
user.prepare('./dfcf.json')

db = pymysql.connect('localhost', 'root', 'root', 'cell')
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)


class CellTrader(object):
    """
        build a cell and trade
    """

    def __init__(self, start, end, level, code, total):
        super(CellTrader, self).__init__()
        (self.__start, self.__end, self.__level, self.__code,
         self.total) = (start, end, level, str(code), total)
        sql = "show tables like '" + self.__code + "'"
        exsist = cursor.execute(sql)
        if not exsist:
            self.__createTable()
            self.__addRecord()
        sql = 'select `price` from `' + self.__code + '` where 1'
        cursor.execute(sql)
        self.__pricelist = cursor.fetchall()
        sql = 'select sum(price * actual_amount)  as total from `' + \
            self.__code + '`'
        cursor.execute(sql)
        data = cursor.fetchall()
        self.__total = float(data[0]['total'])

    def __createTable(self):
        sql = 'create table `' + str(self.__code) + '` (  \
         id int(11) unsigned not null auto_increment, \
         expect_amount int(11) not null ,\
         price decimal(10,3) not null, \
         actual_amount int(11) not null,\
         primary key (id) using btree \
         ) engine=myisam auto_increment = 1 character set = utf8 \
         collate=utf8_general_ci row_format=fixed;'
        cursor.execute(sql)
        db.commit()

    def __addRecord(self):
        sql = 'insert into `' + str(self.__code) + '` (expect_amount, \
        price,actual_amount) values (%s,%s,%s)'
        for i in range(self.__level):
            tmpSql = sql % (1000, self.__start +
                            (self.__end - self.__start) / self.__level * i, 0)
            cursor.execute(tmpSql)
        db.commit()

    def do(self):
        while True:
            today = ts.get_realtime_quotes(self.__code)
            currentPrice = today['price'][0]
            self.__handle(currentPrice)
            print(currentPrice + ' -> ' + time.ctime())
            time.sleep(1)

    def __handle(self, price):
        for idict in self.__pricelist:
            i = str(idict['price'])
            if price == i:
                sql = 'select * from `' + self.__code + '` where price <= ' + \
                    i + ' order by price desc'
                cursor.execute(sql)
                data = cursor.fetchall()
                for item in data[1:]:
                    if item['actual_amount'] != 0:
                        sql = 'select * from `' + self.__code + \
                            '` where price =' + str(item['price'])
                        cursor.execute(sql)
                        data = cursor.fetchone()
                        user.sell(self.__code, price, data['actual_amount'])
                        sql = 'update `' + self.__code + '` set actual_amount = 0 where price=' + \
                            str(item['price'])
                        cursor.execute(sql)
                        db.commit()
                        self.__total -= data['actual_amount'] * float(price)
                        print('sell   ' + time.ctime())
                        break
                else:
                    if data[0]['actual_amount'] == 0 and self.__total < self.total:
                        sql = 'select * from `' + self.__code + '` where price=' + price
                        cursor.execute(sql)
                        data = cursor.fetchone()
                        user.buy(self.__code, price, data['expect_amount'])
                        sql = 'update `' + self.__code + \
                            '` set actual_amount=expect_amount where price =' + price
                        cursor.execute(sql)
                        db.commit()
                        self.__total += data['expect_amount'] * float(price)
                        print('buy   ' + time.ctime())


if __name__ == '__main__':
    cell = CellTrader(1.0, 0.7, 31, 512000, 100000)
    cell2 = CellTrader(1.2, 0.9, 60, 501029, 100000)
    cell3 = CellTrader(1, 0.9, 11, 512980, 10000)
    t1 = Thread(target=cell.do)
    t1.start()
    t2 = Thread(target=cell2.do)
    t2.start()
    t3 = Thread(target=cell3.do)
    t3.start()

