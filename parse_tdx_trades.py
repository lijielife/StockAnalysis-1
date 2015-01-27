# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 20:23:32 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""

import io
import pandas as pd
import numpy as np
from datetime import datetime as dt
import security
from record import TradeRecord
import collections
import sys
pd.set_option('display.encoding', 'utf8')


file_encode = 'gb2312'
codec = 'utf8'


#证券名称,成交日期,成交时间,买卖标志,成交价格,成交数量,成交金额,
#成交编号,委托编号,证券代码,股东代码
_TdxRecordHeader = ['Name', 'Date', 'Time', 'BS', 'Price', 'Volume', 'Amount',
          'TradeNo','OrderNo', 'Code', 'Account']
class TdxRecord (collections.namedtuple('RawRecord', _TdxRecordHeader)):
    _datefmt, _timefmt = "%Y%m%d","%H:%M:%S"
    _bs_state = {u'买入': 'B', u'卖出': 'S'}

    def toRecord(self):
        date = dt.combine(dt.strptime(self.Date,self.__class__._datefmt).date(),
                dt.strptime(self.Time,self.__class__._timefmt).time())
        BS = self.__class__._bs_state.get(self.BS, self.BS)
        code = security.Security(self.Code, self.Name, self.get_market())
        return TradeRecord(date, code, BS, float(self.Price), int(self.Volume))

    def get_market(self):
        if self.Account[0] == 'A':
            return 'SS'
        elif self.Account[0] == '0':
            return 'SZ'

def parse_file(path):
    with io.open(path, 'r') as f:
        f.readline() # header line
        for line in f.readlines():
            cols = (x.strip("=\"") for x in line.rstrip().split("\t"))
            yield TdxRecord(*cols).toRecord()

if __name__ == '__main__':
    path = "D:\\Personal\\Finnance\\Stock\\wt.xls"
    for record in parse_file(path):
        print record

