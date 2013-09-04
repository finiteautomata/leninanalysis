#! coding:utf-8
import numpy
from nltk.corpus import wordnet as wn
from information_value.models import Document
import config
"""
Take the first noun synset
"""

def synset_path_distance(first_synset, second_synset):
    return 1 - wn.path_similarity(first_synset, second_synset)

def __get_noun_synset(word):
    return wn.synset("%s.n.01" % word)

def word_path_distance(word1, word2):
    first_synset = __get_noun_synset(word1)
    second_synset = __get_noun_synset(word2)
    return synset_path_distance(first_synset, second_synset)

def __synset_path_distance(synset1, synset2):
    return 1 - wn.path_similarity(synset1, synset2)


"""

Throws if word is not a noun
"""
def __path_distance_word_to_document(word, doc):
    word_synset = __get_noun_synset(word)
    # There is no noun sense for this word
    # Return the max possible possible

    top_words = [w[0] for w in doc.top_words()]

    distances = []
    for doc_word in top_words:
        try:
            other_synset = __get_noun_synset(doc_word)
            distances.append(__synset_path_distance(word_synset, other_synset))
        except:
            pass
    return numpy.min(distances)

def path_distance(doc1, doc2):
    first_top_words = [w[0] for w in doc1.top_words()]

    distances = []
    for word in first_top_words:
        try: 
            distances.append(__path_distance_word_to_document(word, doc2))
        except:
            pass

    return numpy.average(distances)


def calculate_all_distances(documents, distance=path_distance):
    from pymongo import MongoClient
    client = MongoClient()
    db = client[config.DATABASE_NAME]

    distances = db.distances
    distances.drop()

    index = 0
    for i in xrange(len(documents)):
        doc1 = documents[i]
        for j in xrange(i+1, len(documents)):
            print "Distance from %i to %i" %(i, j)
            doc2 = documents[2]
            distances.insert({
                "id1": doc1._id,
                "id2": doc2._id,
                "index": index,
                "distance": path_distance(doc1, doc2)
            })
            index+=1
