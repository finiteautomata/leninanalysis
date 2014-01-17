#! coding:utf-8
from nltk.corpus import wordnet as wn
from analyzers.synset_analyzer import SynsetAnalyzer
from unittest import TestCase

class JudgeWordTests(TestCase):
    def test_returns_1_for_same_word_as_synsets(self):
        analyzer = SynsetAnalyzer(synsets=[wn.synset("war.n.01")])

        self.assertAlmostEqual(analyzer.judge_word("war"), 1.0)

    def test_returns_less_than_1_for_distinct_words(self):
        analyzer = SynsetAnalyzer(synsets=[wn.synset("war.n.01")])

        self.assertTrue(analyzer.judge_word("music") < 1.0)
