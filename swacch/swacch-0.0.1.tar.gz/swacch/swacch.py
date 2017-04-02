# File for all utility functions in one place

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import json
import io
import time
import subprocess
import sys
import os
import tempfile
import shutil
import codecs
import operator
import heapq
from HTMLParser import HTMLParser
import pkg_resources

resource_package = __name__
resource_path = '/'.join(('data','stopwords.json'))

stopstring = pkg_resources.resource_string(resource_package, resource_path)
stops = json.loads(stopstring)
stops = set(stops)

## Updated with better stopwords lists
def remove_stopwords(sent):
    tokenizer = RegexpTokenizer(r'\w+')
    word_list = tokenizer.tokenize(sent.lower())
    filtered_words = [word for word in word_list if word not in stopwords.words('english')]
    return ' '.join(filtered_words)

## split sentences with a period separator
def split_sentences(text):
    return filter(None,text.lower().split('.'))

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

## strip html tags from text
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
    #return re.sub('[^a-zA-Z\s]', '', s.get_data()).replace('\n',' ')

## remove punctuations from text
def remove_punct(sent):
    tokenizer = RegexpTokenizer(r'\w+')
    return ' '.join(tokenizer.tokenize(sent))

## Yield successive n-sized chunks from list l.
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

## Generate chunks from list
def chunkify(lst,n):
    return [ lst[i::n] for i in xrange(n) ]

## load a file and return its contents
def load_file(loc):
    with codecs.open(loc,'r') as fp:
        return fp.read()

## Calculate Levenshtein Distance between two texts
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

## check if string has numbers
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

## Clean the text with all links, numbers and stopwords
def clean(text):
    text = text.lower()
    # remove links
    text = re.sub(r"http\S+", "", text)
    # text = tokenizer.tokenize(text)
    text = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",text)
    # remove stopwords
    text = [r for r in text if r not in stops]
    # remove numbers
    text = [r for r in text if not hasNumbers(r)]
    return ' '.join(text)

## calculate cosine similarity
def cosine_sim(text1, text2):
    tokenizer = RegexpTokenizer(r'\w+')
    vectorizer = TfidfVectorizer(tokenizer=tokenizer.tokenize,stop_words='english')
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


