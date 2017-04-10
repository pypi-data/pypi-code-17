import numpy as np
import pandas as pd

from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier

# NOTE: Make sure that the class is labeled 'class' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR')
training_indeces, testing_indeces = next(iter(StratifiedShuffleSplit(tpot_data['class'].values, n_iter=1, train_size=0.75)))


result1 = tpot_data.copy()

# Perform classification with a random forest classifier
rfc1 = RandomForestClassifier(n_estimators=62, max_features=min(72, len(result1.columns) - 1))
rfc1.fit(result1.loc[training_indeces].drop('class', axis=1).values, result1.loc[training_indeces, 'class'].values)
result1['rfc1-classification'] = rfc1.predict(result1.drop('class', axis=1).values)
