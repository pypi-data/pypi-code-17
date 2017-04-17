from time import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import redis


def log(msg):
    print(msg)


class ContentBasedRecommendationEngine:

    def __init__(self):
        self.data = pd.DataFrame()
        self.matrix = []
        self._r = []

    def train(self, data):
        """
        :param data: Pandas container -> 2 columns id, desc.
        :return: None
        """
        self.data = data
        start = time()
        self._train()
        log("Engine trained in %s seconds" % (time() - start))

    def _train(self):
        tf = TfidfVectorizer(analyzer='word',
                             ngram_range=(1, 3),
                             min_df=0,
                             stop_words='english')
        tfidf_matrix = tf.fit_transform(self.data['description'])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
        for idx, row in self.data.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [(cosine_similarities[idx][i], self.data['id'][i])
                             for i in similar_indices]
            self._r.append(similar_items)

    def get_similarity_matrix(self):
        return self._r

    def set_similarity_matrix(self, matrix):
        self._r = matrix

    def predict(self, item_id, num):
        """
        Returns a list of tuples containing index of similar entries and their score in descending order

        :param item_id: int
        :param num: int -> number of similar items to return
        :return: A list of tuples like [(0.456567,159), ....]
        """

        return self._r[item_id][1:num+1]
