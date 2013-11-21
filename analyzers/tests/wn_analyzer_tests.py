#! coding:utf-8
from analyzers.wn_analyzer import WordNetAnalyzer
from unittest import TestCase
from nltk.corpus import wordnet as wn


class GetWordSynsetsTest(TestCase):
    def test_get_synsets_for_a_word_return_the_correct_amount_of_synsets(self):
        word = "war"

        self.assertEqual(len(WordNetAnalyzer.get_word_synsets(word)), 4)


class GetInitSynsetsForWordTest(TestCase):
    def test_get_init_synsets_returns_the_correct_amount_of_synsets_(self):
        word = "war"

        synsets = WordNetAnalyzer.get_init_synsets_for_word(word)

        self.assertEqual(len(synsets), 4)
        self.assertAlmostEqual(synsets[0][1], .25)     
        self.assertAlmostEqual(synsets[1][1], .25)
        self.assertAlmostEqual(synsets[2][1], .25)
        self.assertAlmostEqual(synsets[3][1], .25)

