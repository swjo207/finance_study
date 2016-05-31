

class MachineLearningModel(AlphaModel):
	def calcScore(self, split_ratio=0.75, time_lags=10):
		return self.predictor.trainAll(split_ratio=split_ration, time_lags=time_lags)
	
	def determinePosition(self, code, df, column, row_index, verbose=False):
		if (row_index-1) < 0:
			return HOLD

		current_price = df.loc[row_index-1, column]

		prediction_result = 0
		for a_predictor in ['logistic', 'rf', 'svm']:
			predictor = self.predictor.get(code, a_predictor)
			pred, pred_prob = predictor.predict([current_price])
			prediction_result += pred[0]

		if prediction_result > 1:
			return LONG
		else:
			return SHORT


