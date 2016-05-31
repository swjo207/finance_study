from arctic import Arctic

# Connect to Local MONGODB
store = Arctic('localhost')

# Create the library - defaults to VersionStore
store.initialize_library('NASDAQ')

# Access the library
library = store['NASDAQ']

# Load some data - maybe from Quandl
import quandl
quandl.ApiConfig.api_key = "Cxzxjy2eHKXgwMjVFhbH"
aapl = quandl.get("GOOG/NASDAQ_AAPL")

# Store the data in the library
library.write('AAPL', aapl, metadata={'source': 'Quandl'})

# Reading the data
item = library.read('AAPL')
aapl = item.data
metadata = item.metadata

