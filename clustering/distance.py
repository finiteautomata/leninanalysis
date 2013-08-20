#! coding:utf-8
import numpy
from nltk.corpus import wordnet as wn

"""
Take the first noun synset
"""

def __get_noun_synset(word):
    return wn.synset("%s.n.01" % word)

def __word_path_distance(word1, word2):
    first_synset = __get_noun_synset(word1)
    second_synset = __get_noun_synset(word2)
    return 1 - wn.path_similarity(first_synset, second_synset)

def path_distance(doc1, doc2):
    first_top_words = [w[0] for w in doc1.top_words()]
    second_top_words = [w[0] for w in doc2.top_words()]

    return numpy.average([__word_path_distance(w1, w2) for w1, w2 in zip(first_top_words, second_top_words)])
