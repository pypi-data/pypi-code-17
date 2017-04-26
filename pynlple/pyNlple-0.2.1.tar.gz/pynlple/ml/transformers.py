"""
    This module implements custom transformations of Sklearn's Pipeline
"""
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin


class NumFeatureThresholdProbabilityPredictor(BaseEstimator, ClassifierMixin):

    def __init__(self, value_threshold=5, class_thres=0.5):
        self._min_value = value_threshold
        self._thres = class_thres
        self._step = self._thres / self._min_value
        super().__init__()

    def fit(self, X, y):
        self.classes_ = np.unique(y)

    def predict_proba(self, X):
        negative_probas = (X - self._min_value) * self._step
        conditional_negative_probas = np.where(X < self._min_value, -negative_probas, 0.0)
        res = np.vstack(((self._thres + conditional_negative_probas).T, (self._thres - conditional_negative_probas).T))
        return res.T

    def predict(self, X):
        return np.where(self.predict_proba(X)[:,0] < self._thres, *self.classes_)

    def get_params(self, deep=False):
        return {'class_thres': self._thres,
                'value_threshold': self._min_value}


class ThresholdClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, threshold=0.5):
        """Classify samples based on whether they are above of below `threshold`"""
        self.threshold = threshold

    def fit(self, X, y):
        self.classes_ = np.unique(y)
        return self

    def predict(self, X):
        # the implementation used here breaks ties differently
        # from the one used in RFs:
        #return self.classes_.take(np.argmax(X, axis=1), axis=0)
        return np.where(X[:, 0]>self.threshold, *self.classes_)


class ItemSelector(BaseEstimator, TransformerMixin):

    def __init__(self, field_name):
        self.field = field_name

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.field]


class LengthFeature(BaseEstimator, TransformerMixin):

    def __init__(self):
        super().__init__()

    def fit(self, X, y=None):
        return self

    def __length(self, item):
        return len(item)

    def transform(self, X):
        return np.reshape(a=np.array(X.apply(self.__length)), newshape=(-1,1))


class Preprocessor(BaseEstimator, TransformerMixin):

    def __init__(self, preprocessor):
        self.__prep = preprocessor

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(self.__prep.preprocess)

    def get_params(self, deep=False):
        return {'preprocessor': self.__prep}


class ToSeries(BaseEstimator, TransformerMixin):

    def __init__(self):
        super().__init__()

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        from pandas import Series
        import numpy as np
        if type(X) in (list, tuple, np.array):
            X = Series(X)
        return X

    def get_params(self, deep=False):
        return {}


class WSTokenizer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        import re
        pattern = re.compile(r'\s+')
        return X.apply(pattern.split)


class SpaceDetokenizer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(lambda els: ' '.join(els))


class TokenFilterer(BaseEstimator, TransformerMixin):

    def __init__(self, filter):
        self.__filter = filter

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(self.__filter.filter)

    def get_params(self, deep=False):
        return {'filter': self.__filter}


class TextStatsVectorizer(BaseEstimator, TransformerMixin):
    """Extract features from each document with DictVectorizer"""

    def __init__(self):
        self.vectorizer = DictVectorizer(sparse=False, sort=False)

    def fit(self, x, y=None):
        return self

    def get_feature_names(self):
        return self.vectorizer.feature_names_
    
    def __count_text_stats(self, tokens):
        return {
            'contains_exclamation_point': '!' in tokens,
            'contains_url_tag': 'urltag' in tokens,
            'contains_reference': 'atreftag' in tokens,
            'contains_email': 'emailtag' in tokens,
            'contains_digit': '0' in tokens,
        }

    def transform(self, X):
        return self.vectorizer.fit_transform(X.apply(self.__count_text_stats))


class POSVectorizer(BaseEstimator, TransformerMixin):
    """Extract pos as features from each document with DictVectorizer"""

    def __init__(self):
        import pymorphy2
        self.vectorizer = DictVectorizer(sparse=False, sort=False)
        self.morph = pymorphy2.MorphAnalyzer()
        self.PARTS_OF_SPEECH = frozenset([
            'NOUN',  # имя существительное
            'ADJF',  # имя прилагательное (полное)
            'ADJS',  # имя прилагательное (краткое)
            'COMP',  # компаратив
            'VERB',  # глагол (личная форма)
            'INFN',  # глагол (инфинитив)
            'PRTF',  # причастие (полное)
            'PRTS',  # причастие (краткое)
            'GRND',  # деепричастие
            'NUMR',  # числительное
            'ADVB',  # наречие
            'NPRO',  # местоимение-существительное
            'PRED',  # предикатив
            'PREP',  # предлог
            'CONJ',  # союз
            'PRCL',  # частица
            'INTJ',  # междометие
        ])

    def fit(self, x, y=None):
        return self

    def get_feature_names(self):
        return self.vectorizer.feature_names_

    def __get_pos_count(self, tokens):
        rez = dict.fromkeys(self.PARTS_OF_SPEECH, 0)
        if not tokens or len(tokens) <= 0:
            return rez
        for word in tokens:
            pos = self.morph.parse(word)[0].tag.POS
            if pos:
                rez[pos] += 1
        return {k: v / len(list(tokens)) for k, v in rez.items()}

    def transform(self, X):
        return self.vectorizer.fit_transform(X.apply(self.__get_pos_count))
