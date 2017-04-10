import sys
sys.path.append('..')

import pandas as pd
import numpy as np

from xtoy.prep import Sparsify
from xtoy.toys import Toy

from gplearn.genetic import SymbolicTransformer

X = pd.read_csv('/Users/pascal/Downloads/train (1).csv')

X.drop('PassengerId', 1, inplace=True)

y = X['Survived']
X.drop('Survived', 1, inplace=True)

toy = Toy()

gp = SymbolicTransformer(generations=20, population_size=2000,
                         hall_of_fame=100, n_components=10,
                         parsimony_coefficient=0.0005,
                         max_samples=0.9, verbose=1,
                         random_state=0, n_jobs=3)


s = Sparsify().fit(X)

XX = s.transform(X).todense()

XXX = gp.fit_transform(XX, y)

toy.fit(np.hstack((X, np.abs(XXX + np.max(XXX, 0)))), y)

Xtest = np.array(pd.read_csv('/Users/pascal/Downloads/test (1).csv'))

XXXtest = gp.transform(s.transform(Xtest[:, 1:]).todense())

predictions = toy.predict(np.hstack((Xtest[:, 1:], np.abs(XXXtest + np.max(XXXtest, 0)))))

Xtest = np.hstack((np.reshape(Xtest[:, 1], (len(Xtest[:, 1:]), 1)), Xtest[:, 3:]))

predictions = toy.predict(Xtest)

df = pd.DataFrame({'PassengerId': Xtest[:, 0], 'Survived': predictions})
df['Survived'] = df['Survived'].astype(int)
df.to_csv('rsfxridge=10.csv', index=False)

# from sklearn.datasets import load_digits
# digits = load_digits()
# X, y = np.reshape(digits.images, (1797, 8 * 8)), digits.target


# rf n_est = 20
{"clf__min_samples_split": 20, "tsvd__n_iter": 20, "tsvd__n_components": 10, "clf__min_samples_leaf": 5,
    "clf__max_features": "sqrt", "clf__max_depth": 20, "clf__n_estimators": 20, "clf__class_weight": "balanced"}

# ridge
{"clf__alpha": 1.7, "tsvd__n_components": 200, "tsvd__n_iter": 5}

# rf n_est = 200
{"tsvd__n_iter": 5, "clf__min_samples_split": 10, "tsvd__n_components": 100, "clf__class_weight": "balanced",
    "clf__max_features": "log2", "clf__n_estimators": 200, "clf__min_samples_leaf": 5, "clf__max_depth": null}


from sklearn.feature_selection import RFE

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import SGDClassifier

rfe = RFE(LogisticRegression())
rfe.fit(XXd, y)

from sklearn.ensemble import ExtraTreesClassifier
model = ExtraTreesClassifier()
model.fit(XXd, y)
# display the relative importance of each attribute
print(model.feature_importances_)


XXd = XX.todense()


def test_titanic_data():
    z = np.array(pd.read_csv('/Users/pascal/Downloads/train (1).csv'))
    X, y = z[:, 2:], np.array(z[:, 1], dtype=float)
    assert apply_toy_on(X, y) > 0.7


from sklearn.cross_validation import *
from sklearn.metrics import *


def crossval(Xmat, yy, clf, folds=10):
    if Xmat.shape[0] != len(yy):
        raise ValueError('lengths not equal')
    xval = 0
    for train_inds, test_inds in StratifiedShuffleSplit(yy, n_iter=folds, test_size=0.2):
        pred = clf.fit(Xmat[train_inds], yy[train_inds]).predict_proba(Xmat[test_inds])
        score = log_loss(yy[test_inds], np.clip(pred, 0.001, 0.999))
        # for p,yyy in zip(pred, yy[test_inds]):
        #     if p != yyy:
        #         print(yyy)
        # print(pred[:10], np.sum(yy[test_inds] == 0), np.sum(yy==0))
        xval += score
    return xval / folds

import pandas as pd
import numpy as np
data = np.array(pd.read_csv('/Users/pascal/Downloads/9db113a1-cdbe-4b1c-98c2-11590f124dd8.csv'))

test_data = np.array(pd.read_csv(
    '/Users/pascal/Downloads/5c9fa979-5a84-45d6-93b9-543d1a0efc41.csv'))

X, y = data[:, 1:-1], data[:, -1]

ids, XT = test_data[:, 0], test_data[:, 1:]

from sklearn.svm import *
from sklearn.ensemble import *
from sklearn.tree import *
from sklearn.linear_model import *
from sklearn.datasets import *

clfs = [LogisticRegression(),
        LinearSVC(), SVC(), DecisionTreeClassifier(), ExtraTreesClassifier()]

from sklearn.feature_selection import SelectPercentile

from sklearn.feature_selection import RFECV

r = RFECV(RidgeClassifier(), verbose=9, cv=10)
rsx = r.fit_transform(X, y)

rsxt = r.transform(X)

for name, clf in zip(['logistic', 'linearsvc', 'svc',
                      'decisiontree', 'extratrees'],
                     clfs):
    print('{:<15} {}'.format(name, sum([crossval(X, y, clf) for _ in range(10)]) / 10))
    print('{:<15} {}'.format(name, sum([crossval(SX, y, clf) for _ in range(10)]) / 10))

from sklearn.feature_selection import VarianceThreshold

from sklearn.feature_selection import SelectFromModel

clf = RidgeClassifier(normalize=True)
for a in [0.001, 0.01, 0.1, 1, 10, 100, 1000]:
    clf.alpha = a
    print('{:<15} {}'.format(a, sum([crossval(X, y, clf) for _ in range(10)]) / 10))

predictions = RidgeClassifier(normalize=True, alpha=0.01).fit(rsx, y).predict(rsxt)


from gplearn.genetic import SymbolicTransformer

st = SymbolicTransformer(population_size=2000, n_components=3, trigonometric=True)
st.fit(RX, y)

from evolutionary_search import EvolutionaryAlgorithmSearchCV

clf = clfs[-1]

SRX = st.transform(X)

clf.min_samples_leaf = 3
clf.max_depth = 1
clf.min_samples_split = 2
clf.n_estimators = 100

rs = RobustScaler()
RX = rs.fit_transform(X)

print(sum([crossval(np.hstack((k, RX, SRX)), y, kn) for _ in range(10)]) / 10)


def predout(clfs, X):
    n = len(X)
    if not isinstance(clfs, list):
        clfs = [clfs]
    totals = np.zeros((n, 1))
    for clf in clfs:
        totals += np.reshape(np.array([x[1] for x in clf.predict_proba(X)]), (n, 1))
    return np.clip(totals / len(clfs), 0.001, 0.999)

with open('complexsub.csv', 'w') as f:
    header = ',Made Donation in March 2007\n'
    f.write(header + '\n'.join([str(x) + ',' + str(y[0]) for x, y in zip(ids, predictions)]))
