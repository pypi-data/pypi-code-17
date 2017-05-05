import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

import glob, os.path, codecs, json
from collections import Sequence

from .exceptions import ModelNotInitialized

class TopycalBase(Sequence):
    # array of dictionaries/simple objects
    # Doc key is how we reference things.. content key is what we want to model on.
    def __init__(self, document_array, doc_key, content_key, num_topics=10, num_topic_words = 20, num_features = 1000, topic_key='topics', topic_threshold=0.01):
        
        self.num_topics = num_topics
        self.num_topic_words = num_topic_words
        self.num_features = num_features
        self.topic_threshold = topic_threshold
        self.drop_word_len = 4 # will internally drop words shorter than this. i.e. this is the min
        self.docs = document_array
        
        # Where we find stuff...
        self.content_key = content_key
        self.doc_key = doc_key

        # initialize 
        # could make this lazy?
        self.naked_docs = self.get_naked_docs(self.docs, self.content_key)
        self.topic_names = None
        
        # These store the doc topic distributions as well as the associated topic info
        self.doc_topic_distrib = None
        self.topics = None
        
        # output
        self.topic_key = topic_key

    def initialize(self):
        raise Exception("You are trying to initialize the base class. Please initialize a child for a specific topic model")  

    def __len__(self):
        return len(self.docs)
    
    # Returns a tuple of the top topic / score
    def __getitem__(self, index):
        try:
            return self.get_topic_for_doc(index)
        except TypeError:
            raise ModelNotInitialized("Model is not initialized, call <instance>.initialize()")
    
    # Get the top topic/score (this is the default for the iterator)
    # Or if you specify threshold, it will return a vector of tuples
    # Where any topic that has a score >= threshold is returned
    #
    # If you set threshold to 0 it will return the entire topic distribution 
    # for that document.
    def get_topic_for_doc(self, doc_num, threshold=None, force_topicid=False):
        # vector of topic scores (position is topic ID)
        scores = self.doc_topic_distrib[doc_num]
        # if threshold is set, we return a tuple of vectors
        if threshold is not None and threshold >=0:
            
            high_scores_idxs = np.where(scores >= threshold)[0].tolist()
            # contains tuples of topic/score
            output = []
            for topic_id in high_scores_idxs:
                if force_topicid:
                    output.append((topic_id,scores[topic_id]))
                else:
                    output.append((self._resolve_topic(topic_id),scores[topic_id]))
            return output
        else: # simple case of tuple

            # this is the top topic ID (int)
            max_score_idx = np.argmax(scores)
            # name if we have one, else still the ID
            if force_topicid:
                topic = max_score_idx
            else:
                topic = self._resolve_topic(max_score_idx)
            return (topic, scores[max_score_idx])
    
    # Resolve a topic ID to a name (if topic_names is set)
    # Else just return the topic ID (no warning)
    def _resolve_topic(self, topic_id):
        if self.topic_names:
            topic_name = self.topic_names[topic_id]
            return topic_name
        else:
            return topic_id   

    # Makes a list of documents with content only.
    # Must remain same length/order as docs
    def get_naked_docs(self, docs, content_key):
        content_only = []
        for elem in docs:
            try:
                if self.drop_word_len:
                    this_content = ' '.join(word for word in elem[content_key].split() if len(word)>=self.drop_word_len)
                    content_only.append(this_content)
                else:
                    content_only.append(elem[content_key])
            except KeyError: # simpler and probably as memory-efficient as tracking separately
                content_only.append('')
        return content_only
    
    # simple list where position corresponds to topic #
    # e.g. pos 0, -> topic 0, pos 3 -> topic 3, etc..
    def set_topic_names(self, topic_names):
        self.topic_names = topic_names
        
    def get_topics(self, model, feature_names, n_top_words):
        topics = {}
        for topic_idx, topic in enumerate(model.components_):
            topics[topic_idx] = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        return topics

    def vectorize_as_tfidf(self, naked_docs):
        tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                max_features=self.num_features,
                                #ngram_range=self.ngram_range,
                                stop_words='english')
        tfidf = tfidf_vectorizer.fit_transform(naked_docs)
        return (tfidf, tfidf_vectorizer)

    def vectorize_as_tf(self, naked_docs):
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                max_features=self.num_features,
                                #ngram_range=self.ngram_range,
                                stop_words='english')
        tf = tf_vectorizer.fit_transform(naked_docs)
        return (tf, tf_vectorizer)
