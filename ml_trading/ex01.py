import pandas as pd
import pandas_datareader.data as web
import datetime

def download_stock_data(file_name, company_code,
  year_from, month_from, day_from,
  year_to, month_to, day_to):
  start = datetime.datetime(year_from, month_from, day_from)
  end = datetime.datetime(year_to, month_to, day_to)
  df = web.DataReader("%s.KS" % (company_code), "yahoo", start, end)
  df.to_pickle(file_name)

  return df

def load_stock_data(file_name):
	df = pd.read_pickle(file_name)
	return df


