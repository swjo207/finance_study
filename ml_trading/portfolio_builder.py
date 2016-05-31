# -*- coding: UTF-8 -*-
import pandas as pd
from arctic import Arctic
from mean_reversion_model import MeanReversionModel
from machine_learning_model import MachineLearningModel
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class PortfolioBuilder:
	def __init__(self):
		self.symbols = []
		krx = pd.read_csv('krx_market_symbols.csv', dtype=object)
		self.symbols = [x for x in krx['code_google','company']]
		
	def getsymbols():
		return self.symbols 

	def load_data_frame(code):
		db = Arctic('localhost')
		stck = db['KRX_G']
		return stck[code].data
	
	def do_stationary_test(self, column, lags_count=100):
		rows_code = self.getsymbols()
		print(rows_code)	
		return Null
		test_result = {'code':[], 'company':[], 'adf_statistic':[], 'adf_1':[], 'adf_5':[], 'adf_10':[], 'hurst':[], 'halflife': []}
		index = 1
		for a_row_code in rows_code:
			code = a_row_code[0]
			company = a_row_code[1]
			
			#print("... %s of %s: testing stationarity on %s %s" %(index, len(rows_code), code, company)

			a_df = self.load_data_frame(code)
			a_df_column = a_df[column]
			
			if a_df_column.shape[0] > 0:
				test_result['code'].append(code)
				test_result['company'].append(company)
				test_result['hurst'].append(self.mean_reversion_model.calcHurstExponent(a_df_column, lags_count))
				test_result['halflife'].append(self.mean_reversion_model.calcHalfLife(a_df_column))
				test_stat, adf_1, adf_5, adf_10 = self.mean_reversion_model.calcADF(a_df_column)
				test_result['adf_statistic'].append(test_stat)
				test_result['adf_1'].append(adf_1)
				test_result['adf_5'].append(adf_5)
				test_result['adf_10'].append(adf_10)

			index += 1
	
		df_result = pd.DataFrame(test_result)
	
		return df_result		
			
	def rank_stationarity(self, df_stationarity):
		df_stationarity['rank_adf'] = 0
		df_stationarity['rank_hurst'] = 0
		df_stationarity['rank_halflife'] = 0

		halflife_percentile = np.percentile(df_stationarity['halflife'], np.arange(0,100,10)) # quartiles

		for row_index in range(df_stationarity.shape[0]):
			df_stationarity.loc[row_index, 'rank_adf'] = self.assessADF(
														df_stationarity.loc[row_index, 'adf_statistic'], 
														df_stationarity.loc[row_index, 'adf_1'], 	
														df_stationarity.loc[row_index, 'adf_5'], 	
														df_stationarity.loc[row_index, 'adf_10'])
			df_statioinarity.loc[row_index,'rank_hurst'] = self.assessHurst(df_stationarity.loc[row_index,'hurst'])
			df_statioinarity.loc[row_index,'rank_halflife'] = self.assessHalflife(halflife_percentile, df_stationarity.loc[row_index, 'halflife'])
			df_statioinarity['rank'] = df_stationarity['rank_adf']+df_stationarity['rank_hurst']+df_stationarity['rank_halflife']
		return df_stationarity

	def build_universe(self, df_stationarity, column, ratio):
		percentile_column = np.percentile(df_stationarity[column], np.arage(0,100,10))
		ratio_index = np.trunc(ratio * len(percentile_column))
		universe = {}
		for row_index in range(df_stationarity.shape[0]):
			percentile_index = get_percentile_index(percentile_column, df_stationarity.loc[row_index, column])
			if percentile_index >= ratio_index:
				universe[df_stationarity.loc[row_index,'code']] = df_stationarity.loc[row_index,'company']
		return universe
	
			 	
