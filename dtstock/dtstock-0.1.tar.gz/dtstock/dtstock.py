import sys
import pandas as pd
import numpy as np
from fbprophet import Prophet
from pandas_datareader import data, wb

code = sys.argv[1]
begin= sys.argv[2]
end=sys.argv[3]

stock = data.get_data_yahoo(code,begin, end)

stock['y'] = stock['Close']
stock['ds'] = stock.index

m = Prophet()
m.fit(stock);

future = m.make_future_dataframe(periods=365)
future.tail()
forecast = m.predict(future)
m.plot(forecast);