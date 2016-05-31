
from portfolio_builder import PortfolioBuilder

portfolio = PortfolioBuilder()

df_statioinarity = portfolio.do_stationarity_test('price_close')
df_rank = portfolio.rank_stationarity(df_stationarity)
stationarity_codes = portfolio.build_universe(df_rank, 'rank', 0.8)

