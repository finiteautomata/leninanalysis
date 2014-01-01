#! coding:utf-8
from nltk.corpus import wordnet as wn
from unittest import TestCase
from analyzers.similarity import path_similarity
from synsets import get_word_synsets

class PathSimilarityTest(TestCase):    
    def test_similarity_between_the_same_word_should_return_1(self):
        war_ss = [wn.synset("war.n.01")]
        self.assertAlmostEqual(path_similarity(war_ss, war_ss), 1.0)


class GetWordSynsetsTest(TestCase):
    def test_get_synsets_for_a_word_return_the_correct_amount_of_synsets(self):
        word = "war"

        self.assertEqual(len(get_word_synsets(word)), 4)
