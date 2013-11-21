#! coding:utf-8
from analyzers.wn_analyzer import WordNetAnalyzer
from unittest import TestCase

class JudgeWordTests(TestCase):
    def test_returns_1_for_same_word_as_synsets(self):
        ponderated_war_synsets = WordNetAnalyzer.get_init_synsets_for_word("war")
        analyzer = WordNetAnalyzer(ponderated_war_synsets)

        self.assertAlmostEqual(analyzer.judge_word("war"), 1.0)

    def test_returns_less_than_1_for_distinct_words(self):
        ponderated_war_synsets = WordNetAnalyzer.get_init_synsets_for_word("war")
        analyzer = WordNetAnalyzer(ponderated_war_synsets)

        self.assertTrue(analyzer.judge_word("music") < 1.0)
