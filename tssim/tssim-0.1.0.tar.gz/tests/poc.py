
import pandas as pd

from tssim.series import TimeSeries
from tssim.examples import rand_lin_noise, random_walk_limit



ts = TimeSeries(start="2017-04-12", freq="h", periods=100)

#tf1 = TimeFunction(convert, condition=lambda x: x < 20)
#tf2 = TimeFunction(lambda x: x+1)

ts.add("Random Walk", iterated=random_walk_limit(4))
ts.add("Linear", rand_lin_noise)

ts.generate().plot_tracks()
