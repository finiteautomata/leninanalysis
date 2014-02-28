#! coding:utf-8
from nltk.corpus import wordnet as wn


def __max_similarity(synsets1, synsets2, similarity_function):
    similarities = [similarity_function(ss1, ss2) for ss1 in synsets1 for ss2 in synsets2]
    return max(similarities) if len(similarities) != 0 else .0


def path_similarity(synsets1, synsets2):
    return __max_similarity(synsets1, synsets2, wn.path_similarity)


def lch_similarity(synsets1, synsets2):
    return __max_similarity(synsets1, synsets2, wn.lch_similarity)

from nltk.corpus import wordnet_ic
corpus = wordnet_ic.ic('ic-brown.dat')


def lin_similarity(synsets1, synsets2):
    similarity_function = lambda ss1, ss2: wn.lin_similarity(ss1, ss2, corpus)
    return __max_similarity(synsets1, synsets2, similarity_function)


def jcn_similarity(synsets1, synsets2):
    similarity_function = lambda ss1, ss2: wn.jcn_similarity(ss1, ss2, corpus)
    return __max_similarity(synsets1, synsets2, similarity_function)


def res_similarity(synsets1, synsets2):
    similarity_function = lambda ss1, ss2: wn.res_similarity(ss1, ss2, corpus)
    return __max_similarity(synsets1, synsets2, similarity_function)

functions = [path_similarity, lch_similarity, lin_similarity, jcn_similarity, res_similarity]
