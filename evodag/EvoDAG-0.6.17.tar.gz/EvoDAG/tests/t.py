from test_root import X, cl
from EvoDAG import EvoDAG
import numpy as np
import logging
from logging import DEBUG
logging.basicConfig(level=DEBUG)

y = cl.copy()
gp = EvoDAG(generations=np.inf,
            tournament_size=2,
            early_stopping_rounds=100,
            time_limit=0.9,
            multiple_outputs=True,
            seed=0,
            popsize=10000)
gp.X = X
gp.nclasses(y)
gp.y = y
gp.create_population()
assert len(gp.y) == 3


