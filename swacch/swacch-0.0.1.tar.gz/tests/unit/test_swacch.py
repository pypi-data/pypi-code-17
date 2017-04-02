from datetime import date
from swacch import swacch

from tests import *
from tests.helpers import *


class TestSwacch(unittest.TestCase):

    def test_remove_stopwords(self):
        sent = 'The words are in sequence'
        rs = swacch.remove_stopwords(sent)
        self.assertEqual(rs, 'words sequence')

    def test_split_sentences(self):
        sent = 'The words are in sequence. Thats how we type.'
        rs = swacch.split_sentences(sent)
        self.assertEqual(len(rs),2)

    def test_strip_tags(self):
        sent = '<p><b>Hey there!</b> How are you?</p>'
        rs = swacch.strip_tags(sent)
        self.assertEqual(rs,'Hey there! How are you?')

    def test_remove_punct(self):
        sent = 'Hey, how are you doing?'
        rs = swacch.remove_punct(sent)
        self.assertEqual(rs,'Hey how are you doing')

    def test_chunk(self):
        ls = range(10)
        rs = swacch.chunks(ls,3)
        self.assertEqual(len(list(rs)),4)

    def test_chunkify(self):
        ls = range(10)
        rs = swacch.chunkify(ls,3)
        self.assertEqual(len(list(rs)),3)

    def test_levenshtein(self):
        sent1 = 'how'
        sent2 = 'howa'
        rs = swacch.levenshteinDistance(sent1,sent2)
        self.assertEqual(rs,1)

    def test_hasNumbers(self):
        sent1 = 'no numbers'
        rs = swacch.hasNumbers(sent1)
        self.assertEqual(rs,False)
        sent2 = 'has numb3r5'
        rs = swacch.hasNumbers(sent2)
        self.assertEqual(rs,True)

    def test_clean(self):
        sent = '<p>Hey! The weather is awesome! 10/10</p>'
        rs = swacch.clean(sent)
        self.assertEqual(rs,'hey weather awesome')

    def test_cosine(self):
        sent1 = 'cricket'
        sent2 = 'cricket'
        rs = swacch.cosine_sim(sent1,sent2)
        self.assertEqual(rs,1)

