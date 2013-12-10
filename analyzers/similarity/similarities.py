#! coding:utf-8
from nltk.corpus import wordnet as wn
from synsets import get_word_synsets
    



def path_similarity(word1, word2):
    synsets1 = get_word_synsets(word1)
    synsets2 = get_word_synsets(word2)

    similarities = [wn.path_similarity(ss1, ss2) for ss1 in synsets1 for ss2 in synsets2]
    return max(similarities) if len(similarities) != 0 else .0

def lch_similarity(word1, word2):
    synsets1 = get_word_synsets(word1)
    synsets2 = get_word_synsets(word2)

    similarities = [wn.lch_similarity(ss1, ss2) for ss1 in synsets1 for ss2 in synsets2]
    return max(similarities) if len(similarities) != 0 else .0

