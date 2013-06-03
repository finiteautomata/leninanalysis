from __future__ import division
from nltk.corpus import gutenberg
from pymongo import MongoClient
from includes.tokenizer import tokenize
from information_value.analysis import get_optimal_window_size

client = MongoClient()
db = client.moby_dick_database



window_sizes = xrange(100, 6000, 100)
sum_thresholds = [0.0005, 0.001, 0.002, 0.003, 0.005, 0.006, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3 ]


def load_moby_dick_analysis():
    db.drop_collection('analysis')
    tokens = get_moby_dick_tokens()
    analysis_collection = db.analysis
    for sum_threshold in sum_thresholds:
        print "Trying analysis for threshold = %s" % sum_threshold
        window_size, analysis = get_optimal_window_size(tokens, window_sizes, 20, sum_threshold=sum_threshold)
        print analysis
        analysis_collection.insert({
            'sum_threshold': sum_threshold,
            'analysis': analysis.encode()
            })
            
    

def get_moby_dick_tokens():
    moby_dick = gutenberg.raw('melville-moby_dick.txt')
    tokens = tokenize(moby_dick, only_alphanum=True, clean_punctuation=True)
    return [token.lower() for token in tokens]
