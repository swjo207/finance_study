import requests
response = requests.get('https://docs.google.com/spreadsheets/d/16nVO8gsE7OF6xhwtHFn94Ijj-4APBe6XumiSf6eF2yI/pub?gid=0&single=true&output=csv')
assert response.status_code == 200, 'Wrong status code'
import sys
with open('krx_market_symbols.csv','w') as f:
	f.write(response.content)
