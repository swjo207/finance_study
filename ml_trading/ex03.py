#from datareaders.datareader import DataReader
from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
import datetime
from pandas_datareader import data, wb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

DB_NAME = 'stock'
TABLES = {}

def test01():
	tbl = 'codes_kosdaq'
	try:
		db = mysql.connector.connect(user='root', password='duffufk207', database='stock',host='philosymbol.net')
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
		
	cursor = db.cursor(dictionary=True)
	cursor.execute('SELECT * FROM '+tbl)
	lists = [row for row in cursor]
	cursor.close()
	db.close()
	return lists

#dicts = test01()
#for row in dicts:
#	print("{}, {} ".format(row['isu_cd'], row['eng_cor_nm']))

def makeCode(market_type, code):
	if market_type == 1:
		return "%s.KS" % (code)
	elif market_type == 2:
		return "%s.KQ" % (code)
	else:
		return code

def test02():
	market_type = 2
	code = '080010'
	code_yahoo = makeCode(market_type,code)
	start = datetime.datetime(2010, 1, 1)
	end = datetime.datetime(2016, 1, 1)

	try:
		df = data.DataReader("KOSDAQ:080010", 'google',start,end)
		return df
	except:
		print("fatal error occurred")
		return None
		
ret = test02()	
print(ret)
