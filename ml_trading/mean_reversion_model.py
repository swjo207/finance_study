

class MeanReversionModel(AlphaModel):
	def __init__(self):
		self.threshold = 0.8

	def calcADF(self,df):
		adf_result = ts.adfuller(df)
		critical_values = adf_result[4]
	
		return adf_result[0], critical_values['1%'], critical_values['5%'], critical_values['10%']

	def calcHurstExponent(self, df, lags_count=100):
		lags = range(2, lags_count)
		ts = np.log(df)
		
		tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
		poly = np.polyfit(np.log(lags), np.log(tau), 1)

		result = poly[0] * 2.0 
		return result

	def calcHalfLife(self, df):
		price = pd.Series(df)
		lagged_price = price.shift(1).fillna(method="bfill")
		delta = price - lagged_price
		beta = np.polyfit(lagged_price, delta, 1)[0]
		half_life = (-1 * np.log(2) / beta)
	
		return half_life

	def determinePosition(self, df, column, row_index, verbose=False):
		current_price = df.loc[row_index, column]
	
		df_moving_average = pd.rolling_mean(df.loc[0:row_index, column], window=self.window_size)
		df_moving_average = pd.rolling_std(df.loc[0:row_index, column], window=self.window_size)
		
		moving_average = df_moving_average[row_index]
		moving_average_std = df_moving_average_std[row_index] 

		price_arbitrage = current_price - moving_average

		if verbose:
			print("diff=%s, price=%s, moving_average=%s, moving_average_std=%s" % (price_arbitrage, current_price, moving_average, moving_average_std)
		if abs(price_arbitrage) > moving_average_std * self.threshold:
			if np.sign(price_arbitrage) > 0:
				return SHORT
			else:
				return LONG
		return HOLD
