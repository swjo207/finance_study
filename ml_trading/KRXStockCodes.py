# -*- coding: UTF-8 -*-

# 1. import library
import requests
import json
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from datawriters.datawriter import DataWriter

#url = 'http://www.krx.co.kr/por_kor/popup/JHPKOR13008.jsp'
#r = requests.post(url, data={'mkt_typ':'S', 'market_gubun': 'allVal'})
url_krx = 'http://global.krx.co.kr/contents/GLB/99/GLB99000001.jspx'
url_koscom = 'http://datamall.koscom.co.kr/servlet/infoService/SearchIssue'

json_dump = ''

def koscom_get_symbol():
	r = requests.post(url_koscom, data={'flag':'SEARCH', 'marketDisabled': 'null', 'marketBit':'1'})
	soup = BeautifulSoup(r.text,"lxml")
	options = soup.findAll('option')
	stock_list = []

	for option in options:
		if len(option.text) <= 8:
			continue
		stock = {}
		stock['code'] = option.text[1:7]
		stock['company'] = option.text[8:]
		stock['full_code'] = option.get('value')
		stock_list.append(stock)

	json_dump = json.dumps(stock_list,ensure_ascii=False).encode('utf8')
	with open('data/krx_symbols.json', 'w') as f:
		f.write(json_dump)

	DataWriter(writer='mysql', database='stock',user='root',password='duffufk207', table='codes', host='philosymbol.net').save(json.loads(json_dump,encoding='utf-8'))

def kospi_get_symbol():
	r = requests.post(url_krx, data={'market_gubun':'1', 'isu_cdnm':'All', 'code':'jj4tM2s/CYkyaG+C0XvYJoi0yI4SLnm6TdW4TlNBqpwGC1sqg0w2y4aJSOnfdwcc7o6v62sQmfZn5OWj8LCuPEsKQX2qLddZNqpnAlC/Yt3C1Jkw9PxzSJHTcozw9rW7'})
	data = r.json()['block1']
	DataWriter(writer='mysql', database='stock',user='root',password='duffufk207', table='codes_kospi', host='philosymbol.net').save(data)

def kosdaq_get_symbol():
	r = requests.post(url_krx, data={'market_gubun':'2', 'isu_cdnm':'All', 'code':'jj4tM2s/CYkyaG+C0XvYJoi0yI4SLnm6TdW4TlNBqpwGC1sqg0w2y4aJSOnfdwcc7o6v62sQmfZn5OWj8LCuPEsKQX2qLddZNqpnAlC/Yt3C1Jkw9PxzSJHTcozw9rW7'})
	data = r.json()['block1']
	DataWriter(writer='mysql', database='stock',user='root',password='duffufk207', table='codes_kosdaq', host='philosymbol.net').save(data)

kospi_get_symbol()
kosdaq_get_symbol()

import requests

def get_sector(code):
    url = 'http://finance.naver.com/item/main.nhn?code=' + code
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    sector = ""
    h4 = soup.find('h4', {'class':'h_sub sub_tit7'})
    if h4 is not None:
        sector = h4.a.text

    return sector

print get_sector('090470')

def get_sector_daum(code):
    url = 'http://finance.naver.com/item/main.nhn?code=' + code
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    sector = ""
    h4 = soup.find('h4', {'class':'h_sub sub_tit7'})
    if h4 is not None:
        sector = h4.a.text

    return sector
