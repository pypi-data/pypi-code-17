from math import exp
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

from dm_recommendation_engine.utils import min_max_normalize

DEBUG = False


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

        return self._r[item_id][1:num + 1]


class IncorrectDimensionError(Exception):
    pass


class UserRecommendationGenerator:
    def __init__(self):
        self.feature_weights = None
        self.max_actual_rating = None
        self.min_actual_rating = None
        self.max_predicted_rating = None
        self.min_predicted_rating = None
        self.mean_absolute_error = None

    def train(self, rating, *data):
        """
        Recieve the feature matrix from user
        :param data: List of matrix
        :return: weight matrix
        """

        sum = [[0 for i in range(len(j[0]))] for j in data]
        for k in range(len(data)):
            for i in range(len(data[k])):
                for j in range(len(data[k][i])):
                    sum[k][j] += data[k][i][j] * rating[i]
        self.feature_weights = [[i / len(data[0]) for i in j] for j in sum]

        predicted_rating = self._calculate_predicted_rating(data, rating)

        self._calculate_min_max_predicted_rating(predicted_rating)

        self._calculate_min_max_actual_rating(rating)

        normalized_rating = min_max_normalize(rating, self.min_actual_rating, self.max_actual_rating)
        normalized_predicted_rating = []
        for i in range(len(predicted_rating)):
            normalized_predicted_rating.append(min_max_normalize(
                predicted_rating[i], self.min_predicted_rating[i], self.max_predicted_rating[i]
            ))

        # Calculate Mean Absolute Error
        self._calculate_mean_absolute_error(data, normalized_predicted_rating, normalized_rating)

        if DEBUG:
            print("-------DEBUG-------")
            print("Rating:", rating)
            print("Predicted Rating:", predicted_rating)
            print("Normalized Predicted Rating:", normalized_predicted_rating)
            print("Normalized Rating:", normalized_rating)
            print("Mean absolute error:", self.mean_absolute_error)
            print("Feature weights:", self.feature_weights)

    def load_feature_weights(self, weight):
        self.feature_weights = weight

    def get_feature_weight(self):
        return self.feature_weights

    def predict(self, *feature_list):
        if len(feature_list) != len(self.feature_weights):
            raise IncorrectDimensionError("Feature Weight and feature list must have same dimensions ")
        r = 0
        predicted_rating = [0 for i in feature_list]
        for k in range(len(feature_list)):
            for i in range(len(feature_list[k])):
                predicted_rating[k] += feature_list[k][i] * self.feature_weights[k][i]
            predicted_rating[k] = min_max_normalize(
                [predicted_rating[k]], self.min_predicted_rating[k], self.max_predicted_rating[k]
            )[0]
            r += predicted_rating[k] * exp(self.mean_absolute_error[k])
        r /= len(self.feature_weights)
        return r

    def _calculate_mean_absolute_error(self, data, normalized_predicted_rating, normalized_rating):
        self.mean_absolute_error = [0 for i in data]
        for k in range(len(data)):
            for i in range(len(data[k])):
                self.mean_absolute_error[k] += normalized_rating[i] - normalized_predicted_rating[k][i]

    def _calculate_min_max_actual_rating(self, rating):
        self.max_actual_rating = rating[0]
        self.min_actual_rating = rating[0]
        for i in rating:
            if i > self.max_actual_rating:
                self.max_actual_rating = i
            elif i < self.min_actual_rating:
                self.min_actual_rating = i

    def _calculate_min_max_predicted_rating(self, predicted_rating):
        self.max_predicted_rating = [i[0] for i in predicted_rating]
        self.min_predicted_rating = [i[0] for i in predicted_rating]
        for i in range(len(predicted_rating)):
            for j in range(len(predicted_rating[i])):
                if predicted_rating[i][j] > self.max_predicted_rating[i]:
                    self.max_predicted_rating[j] = predicted_rating[i][j]
                if predicted_rating[i][j] < self.min_predicted_rating[i]:
                    self.min_predicted_rating[i] = predicted_rating[i][j]

    def _calculate_predicted_rating(self, data, rating):
        predicted_rating = [[0 for j in i] for i in data]
        for k in range(len(data)):
            for i in range(len(data[k])):
                for j in range(len(data[k][i])):
                    predicted_rating[k][i] = self.feature_weights[k][j] * data[k][i][j]
        return predicted_rating
