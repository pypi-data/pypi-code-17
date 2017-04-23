
import pandas as pd
import numpy as np

import tssim as ts

ser = pd.Series(range(10))

ts1 = ts.TimeSeries(start="2017-04-12", freq="h", periods=100)

ts1.add("Random Walk", iterated=lambda x: x+1)
ts1.add("Linear", ts.random.randint(1, 10))

ts1.generate().plot_tracks()
