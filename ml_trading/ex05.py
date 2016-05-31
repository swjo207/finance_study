import os
import datetime
import time
import csv
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd 
from random import shuffle 

def get_historical_price(instrument, begin, end):
	url = "http://www.google.com/finance/historical"
	params = {
		"q": instrument,
		"startdate": begin.strftime("%Y-%m-%d"),
		"enddate": end.strftime("%Y-%m-%d"),
		"num": 200,
		"start": 0, 
	}
	price_list = []
	running=True	
	while (running):
		response = requests.get(url, params=params)
		html = response.text 
		soup = BeautifulSoup(html,"lxml")
		table = soup.find('table', attrs={'class': 'gf-table historical_price'})
		if table==None:
			running=False
			continue
		rows = table.find_all('tr')
		print(len(rows))
		col_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume'] 
		for row in rows[1:]:
			cols = row.find_all('td')
			cols = [ele.text.strip() for ele in cols]
			price = {}
			for id,val in enumerate(cols):
				price[col_names[id]] = cols[id]
			price['Date'] = datetime.datetime.strptime(price['Date'], '%b %d, %Y').strftime('%Y-%m-%d')
			price_list.append(price)	
		time.sleep(2)
		params["start"] += 200
	return price_list

from arctic import Arctic 

def download_daily_bars(instrument, start, end):
	bars = get_historical_price(instrument,start,end)
	dump = json.dumps(bars, ensure_ascii=False).encode('utf-8')
	df = pd.read_json(dump)
	print(df.head())
	if df.empty:
		return df
	df = df.set_index('Date')
	return df

store = Arctic('localhost')
if 'KRX_G' not in store.list_libraries():
	store.initialize_library('KRX_G')

lib = store['KRX_G']
krx = pd.read_csv('krx_market_symbols.csv', dtype=object)
stocks = [x for x in krx['code_google']]
print(len(stocks), " symbols")
begin = datetime.date(2000,1,1)
end = datetime.date(2016,5,30)

shuffle(stocks)

for i, stock in enumerate(stocks):
	print("%d th code=%s" % (i, stock))
	now = datetime.datetime.now()
	df = download_daily_bars(stock,begin,end)
	if df.empty:
		continue
	lib.write(stock, df, metadata={'source': 'google'}) 
	print("loaded data for: ", stock, datetime.datetime.now() - now)
	time.sleep(3)

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
