#-*- coding: utf-8 -*- 
from __future__ import print_function
from datetime import datetime
import time
import ystockquote

from arctic import Arctic
import collections
import pandas
import pandas as pd
import pprint


################################################
# Loading data
################################################


def get_stock_history(ticker, start_date, end_date):
    data = ystockquote.get_historical_prices(ticker, start_date, end_date)
    df = pandas.DataFrame(collections.OrderedDict(sorted(data.items()))).T
    df = df.convert_objects(convert_numeric=True)
    return df


################################################
# VersionStore: Storing and updating stock data
################################################

arctic = Arctic('localhost')
lst = arctic.list_libraries()
if 'KRX' not in lst:
	arctic.initialize_library('KRX')
	

#################################
# Dealing with lots of data
#################################


#NSYE library
lib = arctic['KRX']

def load_all_stock_history_KRX():
    # 
    krx = pd.read_csv('krx_market_symbols.csv', dtype=object)
    stocks = [x for x in krx['code_yahoo']]
    print(len(stocks), " symbols")
    for i, stock in enumerate(stocks):
			try:
				print("%d th code=%s" % (i, stock))
				now = datetime.now()
				data = get_stock_history(stock, '1980-01-01', '2015-07-07')
				lib.write(stock, data)
				print("loaded data for: ", stock, datetime.now() - now)
			except Exception as e:
				print("Failed for ", stock, str(e))


load_all_stock_history_KRX()
print(len(lib.list_symbols()), " KRX symbols loaded")


def read_all_data_from_lib(lib):
    start = time.time()
    rows_read = 0
    for s in lib.list_symbols():
        rows_read += len(lib.read(s).data)
    print("Symbols: %s Rows: %s  Time: %s  Rows/s: %s" % (len(lib.list_symbols()),
                                                          rows_read,
                                                          (time.time() - start),
                                                          rows_read / (time.time() - start)))


read_all_data_from_lib(lib)
# Symbols: 1315 Rows: 11460225   Rows/s: 2,209,909
