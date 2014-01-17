#! coding:utf-8
from nltk.corpus import wordnet as wn
from analyzers.synset_analyzer import SynsetAnalyzer
from unittest import TestCase

class JudgeSynsetTest(TestCase):
    def test_returns_1_for_same_synset(self):
        analyzer = SynsetAnalyzer(synsets=[wn.synset("war.n.01")])

        self.assertAlmostEqual(analyzer.judge_synset(wn.synset("war.n.01")), 1.0)
