from .base import TopycalBase
from sklearn.decomposition import NMF

class TopycalNMF(TopycalBase):
    
    def initialize(self):
        # TfIdf vectors
        tfidf_vectors, tfidf_vectorizer = self.vectorize_as_tfidf(self.naked_docs)
        nmf = NMF(n_components=self.num_topics, random_state=1,
          alpha=.1, l1_ratio=.5).fit(tfidf_vectors)
        tfidf_feature_names = tfidf_vectorizer.get_feature_names()
        self.topics = self.get_topics(nmf, tfidf_feature_names, self.num_topic_words)
        self.doc_topic_distrib = nmf.transform(tfidf_vectors)
        self.model = nmf
        
