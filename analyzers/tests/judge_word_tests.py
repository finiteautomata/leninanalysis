#! coding:utf-8
from analyzers.wn_analyzer import WordNetAnalyzer
from unittest import TestCase

class JudgeWordTests(TestCase):
    def test_returns_1_for_same_word_as_synsets(self):
        analyzer = WordNetAnalyzer("war")

        self.assertAlmostEqual(analyzer.judge_word("war"), 1.0)

    def test_returns_less_than_1_for_distinct_words(self):
        analyzer = WordNetAnalyzer("war")

        self.assertTrue(analyzer.judge_word("music") < 1.0)
