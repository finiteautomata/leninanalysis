#! coding:utf-8
import nltk
from nltk.corpus import wordnet as wn

"""
Get all the synsets for a word
"""


def get_word_synsets(word, only_nouns=True):
    lemmas = wn.lemmas(word)

    #si no me da lemmas, intento algo
    if len(lemmas) == 0:
        wnl = nltk.WordNetLemmatizer()
        lemmatized_word = wnl.lemmatize(word)
        lemmas = wn.lemmas(lemmatized_word)
        if len(lemmas) == 0:
            return []

    #some distances doesn't handle not-noun words
    synsets = [lemma.synset for lemma in lemmas]

    if only_nouns:
        return [synset for synset in synsets if synset.name.split('.')[1] == 'n']
    else:
        return synsets
