from __future__ import division
from unittest import TestCase, skip
from nltk.corpus import gutenberg
from pymongo import MongoClient
from includes.tokenizer import tokenize
from information_value.analysis import get_optimal_window_size

client = MongoClient()
db = client.moby_dick_database




class MobyDickTests(TestCase):
    window_sizes = xrange(100, 6000, 100)
    sum_thresholds = [0.0005, 0.001, 0.002, 0.003, 0.005, 0.01, 0.05 ]

    @skip('eats all memory')
    def test_top_words_for_moby_dick(self):
        db.drop_collection('analysis')
        tokens = get_moby_dick_tokens()
        analysis_collection = db.analysis
        for sum_threshold in self.sum_thresholds:
            print "Trying analysis for threshold = %s" % sum_threshold
            window_size, analysis = get_optimal_window_size(tokens, self.window_sizes, 20, sum_threshold=sum_threshold)
            print analysis
            analysis_collection.insert({
                'sum_threshold': sum_threshold,
                'analysis': analysis.encode()
                })



def get_moby_dick_tokens():
    moby_dick = gutenberg.raw('melville-moby_dick.txt')
    tokens = tokenize(moby_dick, only_alphanum=True, clean_punctuation=True)
    return [token.lower() for token in tokens]
