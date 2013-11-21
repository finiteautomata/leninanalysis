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

class JudgeSynsetTest(TestCase):

    def test_returns_1_for_synset_contained_in_set(self):
        ponderated_war_synsets = WordNetAnalyzer.get_init_synsets_for_word("war")
        analyzer = WordNetAnalyzer(ponderated_war_synsets)
        # This synset should be in the initial war synset
        war_synset = wn.synset("war.n.01")

        self.assertAlmostEqual(analyzer.judge_synset(war_synset), 1.0)

    def test_returns_less_than_1_for_synset_not_contained(self):
        ponderated_war_synsets = WordNetAnalyzer.get_init_synsets_for_word("war")
        analyzer = WordNetAnalyzer(ponderated_war_synsets)

        music_synset = wn.synset("music.n.01")

        self.assertTrue(analyzer.judge_synset(music_synset) < 1)        


