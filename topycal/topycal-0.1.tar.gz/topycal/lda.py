from .base import TopycalBase
from sklearn.decomposition import LatentDirichletAllocation

class TopycalLDA(TopycalBase):
    
    def initialize(self):
        # Raw Count vectors
        tf_vectors, tf_vectorizer = self.vectorize_as_tf(self.naked_docs)
        lda = LatentDirichletAllocation(n_topics=self.num_topics, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
        lda.fit(tf_vectors)
        tf_feature_names = tf_vectorizer.get_feature_names()
        self.topics = self.get_topics(lda, tf_feature_names, self.num_topic_words)
        self.doc_topic_distrib = lda.transform(tf_vectors)
        self.model = lda