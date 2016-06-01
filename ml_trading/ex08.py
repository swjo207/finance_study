
from portfolio_builder import PortfolioBuilder
import pandas as pd
import numpy as np
portfolio = PortfolioBuilder()

#df_stationarity = portfolio.do_stationarity_test('Close')
#df_stationarity.to_csv('res_stationarity.csv', encoding='utf-8')
df_stationarity = pd.read_csv('res_stationarity.csv', encoding='utf-8') 
df_rank = portfolio.rank_stationarity(df_stationarity)
stationarity_codes = portfolio.build_universe(df_rank, 'rank', 0.8)

