#! coding:utf-8
from unittest import TestCase
from analyzers.similarity import path_similarity
from synsets import get_word_synsets
from nltk.corpus import wordnet as wn

class PathSimilarityTest(TestCase):    
    def test_similarity_between_the_same_word_should_return_1(self):
        self.assertAlmostEqual(path_similarity("war", "war"), 1.0)

    def test_similarity_between_two_words_returns_the_least_distance(self):
        # There is just one synset for these words
        penis_synset = wn.lemmas("penis")[0].synset
        anus_synset = wn.lemmas("vagina")[0].synset

        self.assertAlmostEqual(path_similarity("penis", "vagina"), wn.path_similarity(penis_synset, anus_synset))



class GetWordSynsetsTest(TestCase):
    def test_get_synsets_for_a_word_return_the_correct_amount_of_synsets(self):
        word = "war"

        self.assertEqual(len(get_word_synsets(word)), 4)
